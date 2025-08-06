$target_path = Resolve-Path -Path "../Add-On Israel/Terrdata/objects/Models"
$extra_path = Resolve-Path -Path "./Terrdata/objects/_Models"
$new_path = "./Terrdata/objects/Models"

mkdir $new_path
$new_path = Resolve-Path -Path $new_path

Write-Output("Source: $target_path")
Write-Output("Extra: $extra_path")
Write-Output("Target: $new_path")

# get list of directories in source path
$source_subdirs = Get-ChildItem -Path $target_path -Recurse -Directory
# get list of directories in extra path
$extra_subdirs = Get-ChildItem -Path $extra_path -Recurse -Directory
# create simlinks for each directory in both source and extra paths
foreach ($subdir in $source_subdirs) {
    New-Item -ItemType SymbolicLink -Path "$new_path/$subdir" -Target "$target_path/$subdir"
}

foreach ($subdir in $extra_subdirs) {
    Write-Output("$new_path/$subdir | $extra_path/$subdir")
    New-Item -ItemType SymbolicLink -Path "$new_path/$subdir" -Target "$extra_path/$subdir"
}
