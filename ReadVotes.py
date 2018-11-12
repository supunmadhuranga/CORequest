class ReadVotes:
    def read_votes(self, filename):
        database1 = dict()
        try:
            file = open(filename, "r")
            isError = True
            lineCount = 0
            oldState = ""
            voteList = []
            allLines = file.readlines()
            allLines.append("\n")
            for line in allLines:
                if lineCount > 0:
                    temp = []
                    lineData = line.split(",")
                    if oldState != "" and oldState != lineData[0]:
                        database1.update({oldState: voteList})
                        voteList = []

                    for d in range(1, len(lineData)):
                        temp.append(lineData[d])

                    voteCnt = 0
                    if (len(voteList) > 0):
                        for d in voteList:
                            if d[0] > temp[0]:
                                voteList.insert(voteCnt, temp)
                                break
                            voteCnt = voteCnt + 1
                        if voteCnt == len(voteList):
                            voteList.append(temp)
                    else:
                        voteList.append(temp)

                    oldState = lineData[0]
                isError = False
                lineCount = lineCount + 1
        except:
            isError = True

        if isError:
            return False
        return database1

    def write_votes(self, db, filename):
        isError = False
        if not len(db) > 0:
            return False
        else:
            try:
                file = open(filename, "w+")
                for key, values in db.items():
                    for value in values:
                        value3 = value[3]
                        if not "\n" in value3:
                            value3 = value3 + "\n"
                        file.write(key + "," + value[0] + "," + value[1] + "," + value[2] + "," + value3)
                file.close()
            except:
                isError = True

        return not isError

    def read_abbreviations(self, filename):
        database2 = dict()
        isError = False
        try:
            file = open(filename, "r")
            abbCount = 0
            for line in file.readlines():
                if abbCount > 0:
                    data = line.split(",")
                    database2.update({data[0]: data[1]})
                abbCount = abbCount + 1
        except:
            isError = True

        if isError:
            return False
        return database2

    def number_of_votes(self, db, name, category='popular', numbering='tally', state=None):
        sumOfAllVotes = 0
        sumOfSpecifiedVotes = 0
        isCategoryPopular = False
        isCategoryElectoral = False
        isTally = False
        isPercent = False
        isStateNone = False

        if not db:
            return False
        if name == "":
            return False
        if category == "popular":
            isCategoryPopular = True
        if category == "electoral":
            isCategoryElectoral = True
        if numbering == "tally":
            isTally = True
        if numbering == "percent":
            isPercent = True
        if state is None:
            isStateNone = True

        if isStateNone:
            for key, values in db.items():
                for value in values:
                    if isCategoryPopular:
                        sumOfAllVotes = sumOfAllVotes + int(value[2])
                        if name == value[0]:
                            sumOfSpecifiedVotes = sumOfSpecifiedVotes + int(value[2])
                    elif isCategoryElectoral:
                        sumOfAllVotes = sumOfAllVotes + int(value[3])
                        if name == value[0]:
                            sumOfSpecifiedVotes = sumOfSpecifiedVotes + int(value[3])
                    else:
                        return False

        elif not isStateNone:
            valueList = db.get(state)
            if valueList is not None and len(valueList) > 0:
                for value in valueList:
                    if isCategoryPopular:
                        sumOfAllVotes = sumOfAllVotes + int(value[2])
                        if name == value[0]:
                            sumOfSpecifiedVotes = sumOfSpecifiedVotes + int(value[2])
                    elif isCategoryElectoral:
                        sumOfAllVotes = sumOfAllVotes + int(value[3])
                        if name == value[0]:
                            sumOfSpecifiedVotes = sumOfSpecifiedVotes + int(value[3])
                    else:
                        return False
            else:
                return False

        if isTally:
            return sumOfSpecifiedVotes
        elif isPercent:
            percent = (sumOfSpecifiedVotes / sumOfAllVotes) * 100
            return round(percent, 2)
        else:
            return False

    def popular_votes_performance(self, db, name, numbering, order='max'):
        isMax = True
        if not db:
            return False
        if name == '':
            return False
        if numbering != 'tally' and numbering != 'percent':
            return False

        if order == 'min':
            isMax = False
        elif order != 'max':
            return False

        votesByState = dict()
        rv = ReadVotes()
        for key, values in db.items():
            val = rv.number_of_votes(db, name, 'popular', numbering, key)
            votesByState.update({key:val})

        stateCode = ''
        if isMax:
            max = 0
            maxKey = ''
            cnt = 0
            for key, value in votesByState.items():
                if cnt==0:
                    max = int(value)
                    maxKey = key
                if max < int(value):
                    max = int(value)
                    maxKey = key
                cnt = cnt + 1
            stateCode = maxKey

        if not isMax:
            min = 0
            minKey = ''
            cnt = 0
            for key, value in votesByState.items():
                if cnt == 0:
                    min = int(value)
                    minKey = key
                if min > int(value):
                    min = int(value)
                    minKey = key
                cnt = cnt + 1
            stateCode = minKey
        database2 = rv.read_votes('data/abbreviations.csv')
        stateName = database2.get(stateCode)

        if stateName is None:
            return False
        else:
            return stateName[0][0]

    def candidates_difference(self, db, name1, name2, order='smallest'):
        isSmallest = True
        if not db:
            return False
        if name1 == '':
            return False
        if name2 == '':
            return False
        if order != 'smallest' and order != 'largest':
            return False

        if order == 'largest':
            isSmallest = False

        votesGapByState = dict()
        rv = ReadVotes()
        for key, values in db.items():
            val1 = rv.number_of_votes(db, name1, 'popular', 'percent', key)
            val2 = rv.number_of_votes(db, name2, 'popular', 'percent', key)
            if val1 > val2:
                diff = val1 - val2
                votesGapByState.update({key: diff})
            elif val1 < val2:
                diff = val2 - val1
                votesGapByState.update({key: diff})
            else:
                return False

        stateCode = ''
        if not isSmallest:
            max = 0
            maxKey = ''
            cnt = 0
            for key, value in votesGapByState.items():
                if cnt == 0:
                    max = int(value)
                    maxKey = key
                if max < int(value):
                    max = int(value)
                    maxKey = key
                cnt = cnt + 1
            stateCode = maxKey

        if isSmallest:
            min = 0
            minKey = ''
            cnt = 0
            for key, value in votesGapByState.items():
                if cnt == 0:
                    min = int(value)
                    minKey = key
                if min > int(value):
                    min = int(value)
                    minKey = key
                cnt = cnt + 1
            stateCode = minKey
        database2 = rv.read_votes('data/abbreviations.csv')
        stateName = database2.get(stateCode)

        if stateName is None:
            return False
        else:
            return stateName[0][0]

vt = ReadVotes()
db = vt.read_votes("data/votes.csv")
#val = vt.write_votes(db, "test.csv")
#val = vt.read_abbreviations("data/abbreviations.csv")
#val = vt.number_of_votes(db, "Trump", "popular", "tally", "VA")
#val = vt.number_of_votes(db, "Clinton", "electoral")
#val = vt.number_of_votes(db, "Johnson", "popular", "percent")
#val = vt.number_of_votes(db, "Johnson", "POPULAR", "percent")
#val = vt.number_of_votes(db, "McMullin")
#val = vt.number_of_votes(db, "Trump", "popular", "tally", "VR")
#val = vt.number_of_votes(db, "Johnson", "popular", "Percent")
#vp = vt.popular_votes_performance(db, "Trump", "percent", "min")
#vp = vt.popular_votes_performance(db, "Trump", "percent", "best")
#vp = vt.popular_votes_performance(db, "Clinton", "tally", "min")
cd = vt.candidates_difference(db, 'McMullin', 'Johnson', 'largest')
print(cd)
