from github import Github
import sys
import steam
g1 = Github('token')
repo = g1.get_repo("FurryGamesIndex/games")
issue=repo.get_issue(number=int(sys.argv[1]))
stm=steam.IsSteam("https://github.com/FurryGamesIndex/games/issues/"+str(sys.argv[1]))
if stm!=None:
 issue.create_comment('## Raw yaml:\n'+'```\n'+steam.GetSteamData(stm)+'\n```')
