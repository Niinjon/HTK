# ===== Változók =====
$Hostname = Read-Host "Add meg a Hoszt nevet: "
$IPAddress = Read-Host "Add meg az IP címet: "
$SubnetMask = Read-Host "Add meg az Alhálózati maszkot: "
$DefaultGateway = Read-Host "Add meg az Alapértelmezett átjárót: "
$PreferredDNS = Read-Host "Add meg az Elsődleges DNS címét: "
$DomainName = Read-Host "Add meg a Domain nevet: "
$ZoneName = Read-Host "Add meg a DNS Zóna nevet: "

# ===== Számítógép átnevezése =====
Write-Host "A számítógép átnevezése: $Hostname"
Rename-Computer -NewName $Hostname -Force

# ===== Hálózati adapterek konfigurálása =====
Write-Host "Hálózati beállítások konfigurálása..."
$Interface = Get-NetAdapter | Where-Object { $_.Status -eq "Up" }
$PrefixLength = ($SubnetMask.Split('.') | Where-Object { $_ -eq "255" }).Count * 8
New-NetIPAddress -InterfaceAlias $Interface.Name -IPAddress $IPAddress -PrefixLength $PrefixLength -DefaultGateway $DefaultGateway
Set-DnsClientServerAddress -InterfaceAlias $Interface.Name -ServerAddress $PreferredDNS

# ===== DNS utótag beállítása =====
Write-Host "DNS utótag beállítása..."
Set-DnsClientGlobalSetting -SuffixSearchList @("$DomainName")

# ===== Active Directory és DNS telepítése =====
Write-Host "Szolgáltatások telepítése..."
Install-WindowsFeature -Name AD-Domain-Services, DNS -IncludeManagementTools

# ===== Active Directory tartomány telepítése és DNS konfigurálása =====
Write-Host "Active directory és DNS konfigurálása..."
$SecureAdminPassword = Read-Host "Add meg a tartomány jelszavát: "
Install-ADDForest -DomainName $DomainName -DomainNetbiosName ($DomainName.Split('.')[0]) -SafeModeAdministratorPassword $SecureAdminPassword -InstallDNS -Force -NoRebootOnCompletion

# ===== DNS Zóna létrehozása =====
Write-Host "DNS zóna létrehozása..."
Add-DnsServerPrimaryZone -Name $ZoneName -ZoneFile "$ZoneName.dns"

# ===== Újraindítás =====
Write-Host "Újraindítás a beállítások érvényesítéséhez..."
Restart-Computer -Force