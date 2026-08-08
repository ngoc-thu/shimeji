using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

class Program
{
    static string FindJavaExecutable(string baseDir)
    {
        // 1. Check embedded / portable JRE inside app directory
        string localJreW = Path.Combine(baseDir, "jre", "bin", "javaw.exe");
        if (File.Exists(localJreW)) return localJreW;
        string localJre = Path.Combine(baseDir, "jre", "bin", "java.exe");
        if (File.Exists(localJre)) return localJre;

        string localJavaW = Path.Combine(baseDir, "java", "bin", "javaw.exe");
        if (File.Exists(localJavaW)) return localJavaW;
        string localJava = Path.Combine(baseDir, "java", "bin", "java.exe");
        if (File.Exists(localJava)) return localJava;

        // 2. Check JAVA_HOME
        string javaHome = Environment.GetEnvironmentVariable("JAVA_HOME");
        if (!string.IsNullOrEmpty(javaHome))
        {
            string pathW = Path.Combine(javaHome, "bin", "javaw.exe");
            if (File.Exists(pathW)) return pathW;
            string path = Path.Combine(javaHome, "bin", "java.exe");
            if (File.Exists(path)) return path;
        }

        // 3. Check common Oracle Java path
        string oracleW = @"C:\Program Files\Common Files\Oracle\Java\javapath\javaw.exe";
        if (File.Exists(oracleW)) return oracleW;
        string oracle = @"C:\Program Files\Common Files\Oracle\Java\javapath\java.exe";
        if (File.Exists(oracle)) return oracle;

        // 4. Check PATH environment variable
        string pathEnv = Environment.GetEnvironmentVariable("PATH");
        if (!string.IsNullOrEmpty(pathEnv))
        {
            foreach (string p in pathEnv.Split(Path.PathSeparator))
            {
                try
                {
                    string fullPathW = Path.Combine(p.Trim(), "javaw.exe");
                    if (File.Exists(fullPathW)) return fullPathW;
                    string fullPath = Path.Combine(p.Trim(), "java.exe");
                    if (File.Exists(fullPath)) return fullPath;
                }
                catch { }
            }
        }

        return null;
    }

    [STAThread]
    static void Main()
    {
        string dir = AppDomain.CurrentDomain.BaseDirectory;
        string jarPath = Path.Combine(dir, "Shimeji.jar");

        if (!File.Exists(jarPath))
        {
            MessageBox.Show("Không tìm thấy file Shimeji.jar trong thư mục:\n" + dir, "Lỗi Shimeji", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return;
        }

        string javaExe = FindJavaExecutable(dir);
        if (string.IsNullOrEmpty(javaExe))
        {
            MessageBox.Show("Không tìm thấy Java (JRE/JDK) trên máy tính!\nVui lòng tải Java 8 hoặc cao hơn (hoặc giải nén thư mục jre vào thư mục ứng dụng).", "Thiếu Java Runtime", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        ProcessStartInfo psi = new ProcessStartInfo();
        psi.FileName = javaExe;
        psi.Arguments = "-Xmx512m -jar \"" + jarPath + "\"";
        psi.WorkingDirectory = dir;
        psi.UseShellExecute = true;
        psi.WindowStyle = ProcessWindowStyle.Hidden;

        try
        {
            Process.Start(psi);
        }
        catch (Exception ex)
        {
            MessageBox.Show("Lỗi khi khởi chạy Shimeji: " + ex.Message, "Lỗi Shimeji Launcher", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
}
