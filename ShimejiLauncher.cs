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
        string jarPath = Path.Combine(dir, "Shimeji.jar");

        if (!File.Exists(jarPath))
        {
            MessageBox.Show("Không tìm thấy file Shimeji.jar trong thư mục:\n" + dir, "Lỗi Shimeji", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return;
        }

        string batPath = Path.Combine(dir, "launch.bat");

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
            psi.FileName = "javaw.exe";
            psi.Arguments = "-Xmx512m -jar \"" + jarPath + "\"";
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
            MessageBox.Show("Lỗi khi khởi chạy Shimeji: " + ex.Message, "Lỗi Shimeji Launcher", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
}
