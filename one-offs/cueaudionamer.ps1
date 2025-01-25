$ship = "Navi"
Get-ChildItem -Recurse -filter "*.ogg" | % {
    $folder = ($_.DirectoryName -split "\\")[-1]
    switch ($folder) {
        "_vgmt_acb_ext_cv-2000" {$skin = ""}
        "_vgmt_acb_ext_cv-2100" {$skin = "Mild"}
        "_vgmt_acb_ext_cv-2200" {$skin = "Rebellious"}
        "_vgmt_acb_ext_cv-2004" {$skin = "Skin1"}
        default {return}
    }
    switch ($_.Basename) {
        # "" {$line = "SelfIntro"}
        # "" {$line = "Intro"}
        "login" {$line = "Log"}
        # "" {$line = "Details"}
        "main_1" {$line = "SecIdle1"}
        "main_2" {$line = "SecIdle2"}
        "main_3" {$line = "SecIdle3"}
        "main_4" {$line = "SecIdle4"}
        "main_5" {$line = "SecIdle5"}
        "main_6" {$line = "SecIdle6"}
        "main_7" {$line = "SecIdle7"}
        "main_8" {$line = "SecIdle8"}
        "main_9" {$line = "SecIdle9"}
        "main_10" {$line = "SecIdle10"}
        "touch" {$line = "Sec1"}
        # "" {$line = "Sec2"}
        # "" {$line = "Headpat"}
        "mission" {$line = "Task"}
        "mission_complete" {$line = "TaskC"}
        "mail" {$line = "Mail"}
        "home" {$line = "MissionFin"}
        "expedition" {$line = "Commission"}
        # "" {$line = "Str"}
        # "" {$line = "MissionStart"}
        # "" {$line = "MVP"}
        # "" {$line = "Defeat"}
        # "" {$line = "SkillActivation"}
        # "" {$line = "LowHP"}
        # "" {$line = "Affinity0"}
        # "" {$line = "Affinity1"}
        # "" {$line = "Affinity2"}
        # "" {$line = "Affinity3"}
        # "" {$line = "Affinity4"}
        # "" {$line = "Pledge"}
        # "" {$line = "Extra1"}
        # "" {$line = "Extra2"}
        # "" {$line = "Extra3"}
        # "" {$line = "Extra4"}
        # "" {$line = "Extra5"}
        # "" {$line = "Extra6"}
        # "" {$line = "Extra7"}
        # "" {$line = "Extra8"}
        # "" {$line = "Extra9"}
        # "" {$line = "Extra10"}
        # "" {$line = "Extra11"}
        # "" {$line = "Extra12"}
        "chuxi" {$line = "CNYE"}
        "xinnian" {$line = "CNY"}
        "qingrenjie" {$line = "Valentine"}
        "zhongqiu" {$line = "MidAutumn"}
        "wansheng" {$line = "Halloween"}
        "shengdan" {$line = "Christmas"}
        "huodong" {$line = "Event"}
        "genghuan" {$line = "ChangeModule"}
        "chime_0" {$line = "Chime0"}
        "chime_1" {$line = "Chime1"}
        "chime_2" {$line = "Chime2"}
        "chime_3" {$line = "Chime3"}
        "chime_4" {$line = "Chime4"}
        "chime_5" {$line = "Chime5"}
        "chime_6" {$line = "Chime6"}
        "chime_7" {$line = "Chime7"}
        "chime_8" {$line = "Chime8"}
        "chime_9" {$line = "Chime9"}
        "chime_10" {$line = "Chime10"}
        "chime_11" {$line = "Chime11"}
        "chime_12" {$line = "Chime12"}
        "chime_13" {$line = "Chime13"}
        "chime_14" {$line = "Chime14"}
        "chime_15" {$line = "Chime15"}
        "chime_16" {$line = "Chime16"}
        "chime_17" {$line = "Chime17"}
        "chime_18" {$line = "Chime18"}
        "chime_19" {$line = "Chime19"}
        "chime_20" {$line = "Chime20"}
        "chime_21" {$line = "Chime21"}
        "chime_22" {$line = "Chime22"}
        "chime_23" {$line = "Chime23"}
        default {return}
    }
    $dest = "{0} {2}{1}JP.ogg" -f $ship, $skin, $line
    echo $dest
    $_ | Move-Item -Destination $dest
}
