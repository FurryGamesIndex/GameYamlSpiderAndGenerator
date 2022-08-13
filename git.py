from github import Github
import sys
import steam
import hashlib
import requests
import time

md5 = lambda n:hashlib.md5(n.encode()).hexdigest()[8:-8].lower()

g1 = Github('token')
repo = g1.get_repo("kaixinol/games")
stm=steam.IsSteam("https://github.com/FurryGamesIndex/games/issues/"+sys.argv[1])
stmData=steam.GetSteamData(stm)

if stm!=None:
 stmName=stm[stm.rfind('/',0,len(stm)-1)+1:-1]

# create new branch
 sb = repo.get_branch("ghnmsl")
 repo.create_git_ref(ref='refs/heads/' +md5(stmName) , sha=sb.commit.sha)
# push files

 str_arr = stmData[1][stmData[1].rfind("."):]
 img_data = requests.get(stmData[1]).content
 repo.create_file("assets/"+stmName+"/"+"thumbnail" + str_arr, "assets: games/"+stmName+" thumbnail file", img_data, branch=md5(stmName))
 print(repo.create_file("games/games/"+stmName+".yaml", "games/"+stmName+": new game", stmData[0], branch=md5(stmName)))
 time.sleep(3)
# create PR
 fgi=g1.get_organization('FurryGamesIndex').get_repo('games')
 pr=fgi.create_pull("games/{}".format(stmName), "Created by my bot","master","kaixinol:{}".format(md5(stmName)),True)

 # comment
 issue = fgi.get_issue(number=int(sys.argv[1]))
 issue.create_comment('PR Opened on #{}\n'.format(str(pr.number)))