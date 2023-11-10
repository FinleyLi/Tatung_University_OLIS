# https://ss64.com/ps/messagebox.html
$periodSt = '07:30'
$periodEd = '17:30'
$now = Get-Date -Format 'HH:mm'
if ($now -le $periodSt -or $now -ge $periodEd) { Exit }

Add-Type -AssemblyName System.Windows.Forms,System.Drawing
$frm = New-Object System.Windows.Forms.Form
$frm.TopMost = $true
$frm.Text = 'punch in / out'#'打卡提醒'
$frm.StartPosition = 'CenterScreen'
$frm.FormBorderStyle = 'FixedDialog'
$frm.MaximizeBox = $false
$frm.MinimizeBox = $false
$frm.ControlBox = $true
$frm.ShowInTaskbar = $true
$frm.BackColor = [System.Drawing.Color]::FromArgb(0xff, 0x2d, 0x2e, 0x30)
$img = [System.Drawing.Image]::FromFile("$PSScriptRoot\punch_in_out.png")
$picBox = New-Object System.Windows.Forms.PictureBox
$picBox.Image = $img
$picBox.SizeMode = 'AutoSize'
# 用 Add_Click() 設定點擊事件關閉視窗
$picBox.Add_Click({ $frm.Close() })
$frm.Controls.Add($picBox)
$frm.Width = $img.Width + 20
$frm.Height = $img.Height + 40
$frm.ShowDialog()