using System;

namespace Demo
{
    /// <summary>
    /// This class is entry point for the application
    /// </summary>
    public sealed class AppEntry
    {
        [STAThread]
        static void Main()
        {
            new App.AppWindow().ShowDialog();
        }
    }
}