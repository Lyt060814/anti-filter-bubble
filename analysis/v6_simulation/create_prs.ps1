$ErrorActionPreference = 'Stop'
$ghCommand = Get-Command gh -ErrorAction SilentlyContinue
if ($ghCommand) { $ghExecutable = $ghCommand.Source }
else { $ghExecutable = 'C:\Users\86139\AppData\Local\Microsoft\WinGet\Packages\GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe\bin\gh.exe' }
& $ghExecutable auth status
if ($LASTEXITCODE -ne 0) { throw 'Complete gh auth login --hostname github.com --web locally, then retry. Never paste tokens into chat.' }
$tasks = @(
    @('R1','ruicong/r1-model','Transparent model and numerical self-checks'),
    @('R2','ruicong/r2-formation','Formation scan and population references'),
    @('R3','ruicong/r3-escape','Escape strategies and persistence'),
    @('R4','ruicong/r4-detection','Detection sample and exposure requirements'),
    @('R5','ruicong/r5-report','English simulation section and reproducibility evidence')
)
foreach ($task in $tasks) {
    $existing = & $ghExecutable pr list --repo Lyt060814/anti-filter-bubble --head $task[1] --base main --state open --json url --jq '.[].url'
    if ($LASTEXITCODE -ne 0) { throw 'Unable to query PRs.' }
    if ($existing) { Write-Output $existing; continue }
    & $ghExecutable pr create --repo Lyt060814/anti-filter-bubble --base main --head $task[1] --title "[$($task[0])] $($task[2])" --body-file (Join-Path $PSScriptRoot "pr_bodies/$($task[0]).md")
    if ($LASTEXITCODE -ne 0) { throw "Unable to create $($task[0]) PR." }
}
