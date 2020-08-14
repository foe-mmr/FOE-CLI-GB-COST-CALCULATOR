import os
import pychrome
import json
from collections import OrderedDict
from operator import getitem
from TextFormatter import TextFormatter
from sys import platform

from tabulate import tabulate
import ast

import urllib2

local_version = "v0.1.3"
latest_version = ""
github_url = "https://github.com/foe-mmr/FOE-CLI-GB-COST-CALCULATOR"

otherPlayerOverview = []

class EventHandler:
    def __init__(self, tab, world):
        self.tab = tab
        self.world = world
        self.ARC_bonus = 0
        self.request_cnt = 0

        self.requestIds = []

    
    def handleRequest(self, requestId, **kwargs):
        requestId = requestId.encode('utf-8')

        try:
            request = kwargs.get('request')
            url = request.get('url')

            if self.world in url:

                headers = request.get('headers')
                postdata = request.get('postData')
                postdataFixed = postdata.replace("true","True").replace("false","False").replace("null","None")
                
                data = ast.literal_eval(postdataFixed)

                rc = data[0].get('requestClass')
                rm = data[0].get('requestMethod')

                if (rc == "GreatBuildingsService" and (rm == "getConstruction" or rm == "contributeForgePoints" or rm == "getOtherPlayerOverview")) or (rc == "StartupService" and rm == "getData"):
                    self.requestIds.append(requestId)

        except Exception as e:
            pass

    def handleLoading(self, requestId, **kwargs):
        requestId = requestId.encode('utf-8')

        if requestId not in self.requestIds:
            return False

        try:
            body = self.tab.Network.getResponseBody(requestId=requestId)
            responses = json.loads(body.get('body'))

        except Exception as e:
            responses = []

        hasCityMapService = False
        hasGreatBuildingsService = False

        for r in responses:
            rc = r.get('requestClass')
            rm = r.get('requestMethod')
            rd = r.get('responseData')

            if rc == "GreatBuildingsService" and rm == "getOtherPlayerOverview":
                global otherPlayerOverview
                otherPlayerOverview = rd


            if rc == "CityMapService" and rm == "updateEntity":
                hasCityMapService = True

            if rc == "GreatBuildingsService" and (rm == "getConstruction" or rm == "contributeForgePoints"):
                hasGreatBuildingsService = True

            if hasCityMapService and hasGreatBuildingsService:
                self.processGB(responses)

            if rc == "BonusService" and rm == "getLimitedBonuses":
                for item in rd:
                    if item["type"] == "contribution_boost":
                        bonus = (float(item["value"])+100)/100

                        printClear()
                        print "ARC bonus: ", item["value"],"%"
                        print "Open GB to use calculator"
                        updateWarning()

                        self.ARC_bonus = bonus
                break

            if hasCityMapService and hasGreatBuildingsService:
                break

        self.requestIds.remove(requestId)

    def processGB(self, responses):
        if self.ARC_bonus == 0:
            print "Please refresh FOE to get initial data about ARC bonus"
            return False

        cprint = TextFormatter()
        forge_points_for_level_up = 0
        invested_forge_points = 0
        remaining_fps = 0
        rankings = {}
        gb_name = False
        player_name = False

        for r in responses:
            rc = r.get('requestClass')
            rm = r.get('requestMethod')
            rd = r.get('responseData')

            if rc == "CityMapService":
                forge_points_for_level_up = rd[0]["state"]["forge_points_for_level_up"]
                if 'invested_forge_points' in rd[0]["state"].keys():
                    invested_forge_points = rd[0]["state"]["invested_forge_points"]
                else:
                    invested_forge_points = 0
                remaining_fps = forge_points_for_level_up - invested_forge_points

                if 'player_id' in rd[0].keys() and 'id' in rd[0].keys():
                    gb_id = rd[0]["id"]
                    player_id = rd[0]["player_id"]

                    for gb in otherPlayerOverview:
                        if gb["entity_id"] == rd[0]["id"]:
                            gb_name = gb["name"]
                            player_name = gb["player"]["name"]


            if rc == "GreatBuildingsService" and rm == "getConstruction":
                rankings = rd["rankings"]

            if rc == "GreatBuildingsService" and rm == "contributeForgePoints":
                rankings = rd

        printClear()

        if gb_name and player_name:
            print gb_name
            print player_name,"\n"

        return_data = self.printSpots(rankings, remaining_fps)
        print "Remaining FPs to level: ", remaining_fps

        if len(return_data) > 0:
            if return_data[0] > 0:
                cprint.cfg('g', 'k', 'b')
                print "INVEST: ", cprint.out(return_data[0])
                print "REWARD: ", return_data[1]
            else:
                cprint.cfg('y', 'k', 'b')
                print cprint.out('YOUR SPOT IS SAFE')
                print "REWARD: ", return_data[1]
        else:
            cprint.cfg('k', 'r', 'b')
            print cprint.out('NO PROFIT HERE :(')

        updateWarning()

    def hasFPsInvested(self, rankings):
        fps_invested = 0

        for r in rankings:
            if 'is_self' in r["player"].keys() and r["player"]["is_self"]:
                fps_invested = r["forge_points"]

        return fps_invested

    def secureSelf(self, rankings, remaining_fps):
        fps_invested = 0
        fps_next_spot = 0
        to_lock_a_spot = 0

        for thiselem,nextelem in zip(rankings, rankings[1 : ] + rankings[ : 1]):
            if 'is_self' in thiselem["player"].keys() and thiselem["player"]["is_self"]:
                fps_invested = thiselem["forge_points"]

                if 'forge_points' in nextelem.keys():
                    fps_next_spot = nextelem["forge_points"]

        to_lock_a_spot = (remaining_fps + fps_invested - fps_next_spot)/2+fps_next_spot

        return [fps_next_spot, to_lock_a_spot]


    def printSpots(self, rankings, remaining_fps):
        cprint = TextFormatter()

        table = []
        found_what_to_snipe = False
        return_data = []
        found_self = False

        fps_already_invested = self.hasFPsInvested(rankings)

        for r in rankings:
            rank = "-"
            name = ""
            forge_points = 0
            to_lock_a_spot = 0
            total_fps_for_spot = 0
            reward = 0
            profit = "LOCKED"
            profitable_spot = 0
            is_self = False

            if 'is_self' in r["player"].keys() and r["player"]["is_self"]:
                is_self = True

            if 'rank' in r.keys():
                rank = r["rank"]

            if 'reward' in r.keys():
                if 'strategy_point_amount' in r["reward"].keys():
                    reward = int(round(float(r["reward"]["strategy_point_amount"])*self.ARC_bonus))

            if 'forge_points' in r.keys():
                forge_points = r["forge_points"]

            cprint.cfg('w', 'k', 'f')

            if not is_self:
                if found_self and rank < 6:
                    cprint.cfg('w', 'k', 'f')

                    table.append([rank, cprint.out("-"), cprint.out("-")])
                    continue

                to_lock_a_spot = int(round((float(remaining_fps) + forge_points - fps_already_invested)/2))


                if to_lock_a_spot + fps_already_invested <= forge_points:
                    cprint.cfg('r', 'k', 'b')
                    to_lock_a_spot = "LOCKED"
                else:
                    profit = reward-to_lock_a_spot-fps_already_invested
                    total_fps_for_spot = to_lock_a_spot

                    if fps_already_invested > 0:
                        total_fps_for_spot = to_lock_a_spot+fps_already_invested
                    if profit > 0:
                        return_data = [to_lock_a_spot, profit, rank]
                        cprint.cfg('g', 'k', 'x')

                    found_what_to_snipe = True
            else:
                found_self = True
                data = self.secureSelf(rankings, remaining_fps)
                total_fps_for_spot = data[1]
                to_lock_a_spot = data[1] - fps_already_invested
                profit = reward-to_lock_a_spot-fps_already_invested

                if profit > 0:
                        return_data = [to_lock_a_spot, profit, rank]
                        cprint.cfg('g', 'k', 'x')

                if to_lock_a_spot < 1:
                    cprint.cfg('y', 'k', 'b')
                    found_what_to_snipe = True

            if rank < 6:
                rank = cprint.out(rank)
                name = cprint.out(name)
                forge_points = cprint.out(forge_points)
                if fps_already_invested > 0 and total_fps_for_spot > fps_already_invested:
                    str_print = str(to_lock_a_spot)+" ("+str(total_fps_for_spot)+")"
                    to_lock_a_spot = cprint.out(str_print)
                else:
                    to_lock_a_spot = cprint.out(to_lock_a_spot)
                reward = cprint.out(reward)

                if profit < 0:
                    cprint.cfg('r', 'k', 'b')

                profit = cprint.out(profit)

                #table.append([rank, name, forge_points, to_lock_a_spot, reward, profit])
                table.append([rank, to_lock_a_spot, profit])

        print(tabulate(table, headers=['#', 'Cost', 'Difference']))
        return return_data


def printClear(do_print = True):
    if do_print:
        os.system('cls||clear')

def getVersion():
    response = urllib2.urlopen("https://api.github.com/repos/foe-mmr/FOE-CLI-GB-COST-CALCULATOR/releases/latest")
    data = json.load(response)
    global latest_version
    latest_version = data.get('tag_name')

def updateWarning():
    if local_version != latest_version:
        print "!!!"
        print "!!! You are not using Latest version of script"
        print "!!! Please update to", latest_version
        print github_url

def main():
    getVersion()

    init_FOE = True
    tabs = False

    show_msg_1 = True

    printClear()
    print "Open Chrome with remote debugger or run 'python open_chrome.py'"
    print "Then open FOE in that window"

    updateWarning()

    
    while init_FOE:
        browser = pychrome.Browser(url='http://127.0.0.1:9222')
        
        try:
            tabs = browser.list_tab()
        except:
            return False

        for tab in browser.list_tab():
            tab.start()
            node = tab.DOM.getDocument()
            url = node['root']['documentURL']     
            
            world, domain = url[8:].split('.', 1)

            if 'forgeofempires.com/game' in url:
                eh = EventHandler(tab, world)
                tab.Network.loadingFinished = eh.handleLoading
                tab.Network.requestWillBeSent = eh.handleRequest

                tab.Network.enable()

                init_FOE = False

                printClear()

                if eh.ARC_bonus == 0:
                    print "Please refresh FOE to get initial data about ARC bonus"
                else:
                    print "Open GB"

                updateWarning()
        
if __name__ == '__main__':
    main()
    raw_input()
