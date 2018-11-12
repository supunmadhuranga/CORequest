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

vt = ReadVotes()
#db = vt.read_votes("data/votes.csv")
#val = vt.write_votes(db, "test.csv")
val = vt.read_abbreviations("data/abbreviations.csv")
print(val)
