using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

class Program
{
    [STAThread]
    static void Main()
    {
        string dir = AppDomain.CurrentDomain.BaseDirectory;
        string batPath = Path.Combine(dir, "run-settings.bat");
        string scriptPath = Path.Combine(dir, "shimeji_settings.py");

        if (!File.Exists(scriptPath))
        {
            MessageBox.Show("Không tìm thấy file shimeji_settings.py trong thư mục:\n" + dir, "Lỗi Shimeji Settings", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return;
        }

        ProcessStartInfo psi = new ProcessStartInfo();
        if (File.Exists(batPath))
        {
            psi.FileName = batPath;
            psi.WorkingDirectory = dir;
            psi.WindowStyle = ProcessWindowStyle.Hidden;
            psi.UseShellExecute = true;
        }
        else
        {
            psi.FileName = "pythonw.exe";
            psi.Arguments = "\"" + scriptPath + "\"";
            psi.WorkingDirectory = dir;
            psi.WindowStyle = ProcessWindowStyle.Hidden;
            psi.UseShellExecute = true;
        }

        try
        {
            Process.Start(psi);
        }
        catch (Exception ex)
        {
            MessageBox.Show("Lỗi khi khởi chạy Shimeji Settings: " + ex.Message, "Lỗi Shimeji Settings Launcher", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
}
