# Tatung_University_OLIS
- 🔧 System guru, sailing the code sea. 
- 🌐 Network ninja, guarding our digital fort. 
- 💾 Data wizard, safeguarding bytes. 
- 🤝 User whisperer, solving tech puzzles. 
- ✨ IT magic in action! ✨

## 📚 About Me
- 🎓 I’m a dedicated staff member at the Computer Center of Tatung University.
- 🌱 My expertise lies in Python, Java, SQL, data center management, and more. Always learning, always growing!

## 📫 How to reach me
- 📧 Email: [Finley](mailto:fanli@gm.ttu.edu.tw)
- 📱 Phone: [+886-2-21822928-6903](tel:+886221822928)

## 📊 Step by Step
* install Git [git website](https://git-scm.com/download/win)--fast-version-control
* check version`git --version`
* create key `ssh-keygen -t ed25519 -C "username@domain"`
* start ssh-agent `eval "$(ssh-agent -s)"`
* cat ~/.ssh/id_ed25519.pub
    - `ssh-ed25519 ... username@domain`
    - 頭像 > Settings > SSH and GPG keys > Add SSH key。
* VSCode 輸入
    - `Ctrl + Shift + P`
    - `Git: Clone`
* git base use
    - `git config --global user.name "username"`
    - `git config --global user.email "username@domain"`
    - `git config --list`
    - 輸入 `git pull` 更新
    - 輸入 `git add .` 加入檔案
    - 輸入 `git commit -m "message"` 註解
    - 輸入 `git push` 上傳
    - 輸入 `git status` 查看狀態
    - 輸入 `git log` 查看紀錄
* git branch
    - 輸入 `git branch` 查看分支
    - 輸入 `git branch -a` 查看遠端分支
    - 輸入 `git branch -d <branchname>` 刪除分支
    - 輸入 `git checkout <branchname>` 切換分支
    - 輸入 `git checkout -b <branchname>` 建立分支
    - 輸入 `git merge <branchname>` 合併分支
* git tag
    - 輸入 `git tag` 查看標籤
    - 輸入 `git tag -a <tagname> -m "message"` 建立標籤
    - 輸入 `git tag -d <tagname>` 刪除標籤
    - 輸入 `git push origin <tagname>` 上傳標籤
    - 輸入 `git push origin --tags` 上傳全部標籤
    - 輸入 `git push origin :refs/tags/<tagname>` 刪除遠端標籤
    - 輸入 `git checkout <tagname>` 切換標籤
    - 輸入 `git checkout -b <branchname> <tagname>` 建立分支並切換標籤
    - 輸入 `git push origin <branchname>` 上傳分支