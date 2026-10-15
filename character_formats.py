"""Read image references from Shimeji-EE XML and legacy_default_v1 bundles.

Only image references are interpreted; expressions and behavior code are not run.
"""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath

MAX_METADATA_BYTES = 4 * 1024 * 1024


def reference(base, value):
    value = value.replace("\\", "/")
    if value.startswith("/") or ":" in value or ".." in value.split("/"):
        raise ValueError("Unsafe image or metadata path: " + value)
    return str(PurePosixPath(base) / value).casefold()


def _read(entry, opener):
    with opener(entry) as stream:
        data = stream.read(MAX_METADATA_BYTES + 1)
    if len(data) > MAX_METADATA_BYTES:
        raise ValueError("Animation metadata exceeds 4 MiB.")
    return data


def _xml_frames(folder, entry, index, opener, mapping):
    data = _read(entry, opener)
    # Reject UTF-8 and UTF-16 DTDs before ElementTree can expand internal entities.
    if b"<!doctype" in data.replace(b"\x00", b"").lower() or b"<!entity" in data.replace(b"\x00", b"").lower():
        raise ValueError("DTDs and entities are not allowed in animation files.")
    document = ET.fromstring(data)
    actions = {}
    for node in document.iter():
        if node.tag.split("}")[-1] == "Action" and node.get("Name"):
            poses = [p.get("Image") for p in node.iter() if p.tag.split("}")[-1] == "Pose" and p.get("Image")]
            if poses:
                actions[node.get("Name")] = poses
    if not all(name in actions for name in ("Stand", "Walk", "Falling")):
        raise ValueError("The XML file does not contain supported Stand, Walk and Falling animations.")
    frames = {}
    for number, action, pose, _, _ in mapping:
        if action not in actions:
            alias = {"SitAndSpinHeadAction": "HappyJumpAction", "Divide1": "PullUpShimeji1"}.get(action)
            action = alias if alias in actions else "Stand"
        poses = actions[action]
        path = reference(folder, poses[min(pose, len(poses) - 1)].lstrip("/"))
        if path not in index or not path.endswith(".png"):
            raise ValueError("PNG referenced by the XML file is missing: " + path)
        frames[f"shime{number}.png"] = index[path]
    return frames


def _mobile_frames(folder, entry, index, opener, mapping):
    manifest = json.loads(_read(entry, opener))
    schema, sprites = manifest.get("animationSchema", {}), manifest.get("sprites", {})
    if manifest.get("schemaVersion") != 1 or schema.get("schemaId") != "legacy_default_v1" or schema.get("version") != 1 or sprites.get("type") != "SEQUENCE":
        raise ValueError("Unsupported manifest/animation format (expected legacy_default_v1, version 1).")
    animation_path = reference(folder, schema.get("path", "animation.json"))
    if animation_path not in index:
        raise ValueError("Animation metadata is missing: " + animation_path)
    animation = json.loads(_read(index[animation_path], opener))
    if animation.get("schema_id") != "legacy_default_v1" or animation.get("version") != 1:
        raise ValueError("Unsupported JSON animation schema.")
    actions = {a["key"]: a["frames"] for a in animation.get("animations", []) if a.get("frames")}
    if not all(name in actions for name in ("stand_left", "walk_left", "fall")):
        raise ValueError("Standing, walking or falling animation is missing from the JSON package.")
    pattern = sprites.get("filePattern", "")
    if not re.fullmatch(r"%0?[1-9]?\d?d\.(webp|png)", pattern):
        raise ValueError("Unsupported sprite filename pattern: " + pattern)
    count = sprites.get("spriteCount", 0)
    if type(count) is not int or not 1 <= count <= 10000:
        raise ValueError("Invalid sprite count in the manifest.")
    base = reference(folder, sprites.get("basePath", "sprites/"))
    frames = {}
    for number, _, _, action, pose in mapping:
        poses = actions.get(action, actions["stand_left"])
        sprite = poses[min(pose, len(poses) - 1)].get("sprite")
        if type(sprite) is not int or not 0 <= sprite < count:
            raise ValueError("Invalid sprite index in " + action)
        path = reference(base, pattern % sprite)
        if path not in index:
            raise ValueError("Referenced sprite is missing: " + path)
        frames[f"shime{number}.png"] = index[path]
    return manifest.get("name") or PurePosixPath(folder).name, frames


def prepare_groups(entries, fallback, frame_names, opener):
    index, original, groups = {}, {}, {}
    for path, entry in entries:
        key = str(PurePosixPath(path)).casefold()
        if key in index:
            raise ValueError("Duplicate file in package: " + path)
        index[key], original[key] = entry, str(PurePosixPath(path))
        parts = PurePosixPath(path)
        if parts.name.lower() in frame_names:
            groups.setdefault(str(parts.parent), {})[parts.name.lower()] = entry
    mapping = json.loads(Path(__file__).with_name("character_frames.json").read_text(encoding="utf-8"))
    # Named PNG packs may omit shime1.png entirely. Only consider an image folder with its own XML.
    for key in index:
        if key == "conf/actions.xml" or key.endswith("/conf/actions.xml"):
            folder = original[key][:-len("/conf/actions.xml")] if key != "conf/actions.xml" else "."
            if any(str(PurePosixPath(p).parent).casefold() == folder.casefold() and p.endswith(".png") for p in index):
                groups.setdefault(folder, {})
    result = []
    for folder, frames in sorted(groups.items()):
        missing = [name for name in frame_names if name not in frames]
        if missing:
            xml = reference(folder, "conf/actions.xml")
            if xml not in index:
                raise ValueError(f"Incomplete character in {folder}: Missing {', '.join(missing)}")
            frames = _xml_frames(folder, index[xml], index, opener, mapping)
        parts = PurePosixPath(folder)
        label = parts.parent.name if parts.name.lower() in ("img", "images") else parts.name
        result.append((label or fallback, frames))
    for key, entry in index.items():
        if PurePosixPath(key).name == "manifest.json":
            folder = str(PurePosixPath(key).parent)
            label, frames = _mobile_frames(folder, entry, index, opener, mapping)
            result.append((label or fallback, frames))
    if not result:
        raise ValueError("No supported Shimeji images found. Expected standard PNGs, a PNG/XML package or a legacy_default_v1 package.")
    return result
