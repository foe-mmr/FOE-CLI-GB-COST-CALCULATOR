import pychrome
import json
from collections import OrderedDict
from operator import getitem
from TextFormatter import TextFormatter

from tabulate import tabulate
import ast

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

                
                data = ast.literal_eval(postdata)

                rc = data[0].get('requestClass')
                rm = data[0].get('requestMethod')

                if (rc == "GreatBuildingsService" and rm == "getConstruction") or rc == "StartupService" and rm == "getData":
                    self.requestIds.append(requestId)

            if len(postdata) > 10:
                postdatalist = json.loads(postdata)

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

            if rc == "CityMapService":
                hasCityMapService = True

            if rc == "GreatBuildingsService":
                hasGreatBuildingsService = True

            if hasCityMapService and hasGreatBuildingsService:
                self.processGB(responses)

            if rc == "BonusService" and rm == "getLimitedBonuses":
                for item in rd:
                    if item["type"] == "contribution_boost":
                        bonus = (float(item["value"])+100)/100

                        print(chr(27) + "[2J")
                        print "ARC bonus: ", item["value"],"%"
                        print "Open GB to use calculator"

                        self.ARC_bonus = bonus
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

        for r in responses:
            rc = r.get('requestClass')
            rm = r.get('requestMethod')
            rd = r.get('responseData')

            if rc == "CityMapService":
                forge_points_for_level_up = rd[0]["state"]["forge_points_for_level_up"]
                invested_forge_points = rd[0]["state"]["invested_forge_points"]
                remaining_fps = forge_points_for_level_up - invested_forge_points

            if rc == "GreatBuildingsService":
                rankings = rd["rankings"]

        print(chr(27) + "[2J")
        return_data = self.printSpots(rankings, remaining_fps)
        print "Remaining FPs to level: ", remaining_fps

        if len(return_data) > 0:
            cprint.cfg('g', 'k', 'b')
            print "INVEST: ", cprint.out(return_data[0])
            print "REWARD: ", return_data[1]
        else:
            cprint.cfg('k', 'r', 'b')
            print cprint.out('NO PROFIT HERE :(')

    def printSpots(self, rankings, remaining_fps):
        cprint = TextFormatter()

        table = []
        found_what_to_snipe = False
        return_data = []

        for r in rankings:
            rank = "-"
            name = ""
            forge_points = 0
            to_lock_a_spot = 0
            reward = 0
            profit = 0
            profitable_spot = 0

            if 'rank' in r.keys():
                rank = r["rank"]

            if 'reward' in r.keys():
                if 'strategy_point_amount' in r["reward"].keys():
                    reward = int(round(float(r["reward"]["strategy_point_amount"])*self.ARC_bonus))

            name = r["player"]["name"]

            if 'forge_points' in r.keys():
                forge_points = r["forge_points"]

            cprint.cfg('w', 'k', 'f')

            if forge_points >= remaining_fps and rank != '-':
                cprint.cfg('r', 'k', 'b')

            if found_what_to_snipe == False and rank < 6 and forge_points < remaining_fps:
                to_lock_a_spot = int(round(((float(remaining_fps) - forge_points) / 2) + forge_points))
                profit = reward-to_lock_a_spot

                found_what_to_snipe = True
                if profit > 0:
                    cprint.cfg('g', 'k', 'x')
                    return_data = [to_lock_a_spot, profit, rank]
                else:
                    cprint.cfg('r', 'k', 'b')

            if rank == '-':
                cprint.cfg('y', 'k', 'f')

            if rank < 6:
                rank = cprint.out(rank)
                name = cprint.out(name)
                forge_points = cprint.out(forge_points)
                to_lock_a_spot = cprint.out(to_lock_a_spot)
                profit = cprint.out(profit)
                reward = cprint.out(reward)

                #table.append([rank, name, forge_points, to_lock_a_spot, reward, profit])
                table.append([rank, to_lock_a_spot, profit])

        print(tabulate(table, headers=['#', 'Cost', 'Difference']))
        return return_data

def main():
    init_FOE = True
    tabs = False

    show_msg_1 = True

    print(chr(27) + "[2J")
    print "Open Chrome with remote debugger or run 'python open_chrome.py'"
    print "Then open FOE in that window"

    
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
                print(chr(27) + "[2J")
                if eh.ARC_bonus == 0:
                    print "Please refresh FOE to get initial data about ARC bonus"
                else:
                    print "Open GB"
        
if __name__ == '__main__':
    main()
    raw_input()
