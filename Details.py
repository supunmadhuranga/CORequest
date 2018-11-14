def read_votes(filename):
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
                    if d < 3:
                        temp.append(lineData[d].strip())
                    else:
                        temp.append(int(lineData[d].strip()))

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


def write_votes(db, filename):
    isError = False
    if not len(db) > 0:
        return False
    else:
        try:
            file = open(filename, "w+")
            for key, values in db.items():
                for value in values:
                    value3 = value[3]
                    # if not "\n" in value3:
                    #     value3 = value3 + "\n"
                    file.write(key + "," + value[0] + "," + value[1] + "," + str(value[2]) + "," + str(value3) + '\n')
            file.close()
        except:
            isError = True

    return not isError


def read_abbreviations(filename):
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


def number_of_votes(db, name, category='popular', numbering='tally', state=None):
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


def popular_votes_performance(db, name, numbering, order='max'):
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
    for key, values in db.items():
        val = number_of_votes(db, name, 'popular', numbering, key)
        votesByState.update({key: val})

    stateCode = ''
    if isMax:
        max = 0
        maxKey = ''
        cnt = 0
        for key, value in votesByState.items():
            if cnt == 0:
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
    database2 = read_abbreviations('abbreviations.csv')
    stateName = database2.get(stateCode)

    if stateName is None:
        return False
    else:
        return stateName.strip()


def candidates_difference(db, name1, name2, order='smallest'):
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
    for key, values in db.items():
        val1 = number_of_votes(db, name1, 'popular', 'percent', key)
        val2 = number_of_votes(db, name2, 'popular', 'percent', key)
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
    database2 = read_abbreviations('abbreviations.csv')
    stateName = database2.get(stateCode)

    if stateName is None:
        return False
    else:
        return stateName.strip()


def remove_candidate(db, name, state=None):
    if state is not None:
        votesInState = db.get(state)
        if votesInState is not None:
            for det in votesInState:
                if name == det[0]:
                    votesInState.remove(det)
                    if len(votesInState) > 0:
                        db.update({state: votesInState})
                    else:
                        del db[state]
                    return None
        else:
            return False
    else:
        for key, values in db.items():
            votesInState = db.get(key)
            if votesInState is not None:
                for det in votesInState:
                    if name == det[0]:
                        votesInState.remove(det)
                        if len(votesInState) > 0:
                            db.update({key: votesInState})
                        else:
                            del db[key]
        return None


def incorporate_precinct(db, name, state, popular_votes_increment):
    votesInState = db.get(state)
    if votesInState is not None:
        count = 0
        for det in votesInState:
            if name == det[0]:
                existingVotes = int(det[2])
                det[2] = existingVotes + popular_votes_increment
                votesInState[count] = det
                db.update({state: votesInState})
                return None
            count = count + 1
        return False
    else:
        return False


def merge_votes(db, name1, name2, new_name, new_party, state=None):
    if state is not None:
        votesInState = db.get(state)
        candidate1PopVotes = 0
        candidate1ElVotes = 0
        candidate2PopVotes = 0
        candidate2ElVotes = 0
        newVote = []
        isName1 = False
        isName2 = False
        for det in votesInState:
            if name1 == det[0]:
                candidate1PopVotes = int(det[2])
                candidate1ElVotes = int(det[3])
                isName1 = True
            if name2 == det[0]:
                candidate2PopVotes = int(det[2])
                candidate2ElVotes = int(det[3])
                isName2 = True

            if isName1 and isName2:
                break
        newVote = [new_name, new_party, candidate1PopVotes + candidate2PopVotes,
                   candidate1ElVotes + candidate2ElVotes]
        votesInState.append(newVote)
        db.update({state: votesInState})
        return None
    else:
        for key, value in db.items():
            votesInState = db.get(key)
            candidate1PopVotes = 0
            candidate1ElVotes = 0
            candidate2PopVotes = 0
            candidate2ElVotes = 0
            newVote = []
            isName1 = False
            isName2 = False
            for det in votesInState:
                if name1 == det[0]:
                    candidate1PopVotes = int(det[2])
                    candidate1ElVotes = int(det[3])
                    isName1 = True
                if name2 == det[0]:
                    candidate2PopVotes = int(det[2])
                    candidate2ElVotes = int(det[3])
                    isName2 = True

                if isName1 and isName2:
                    break
            newVote = [new_name, new_party, candidate1PopVotes + candidate2PopVotes,
                       candidate1ElVotes + candidate2ElVotes]
            votesInState.append(newVote)
            db.update({key: votesInState})
        return None
