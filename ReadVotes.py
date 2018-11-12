class ReadVotes:
    def read_votes(self, filename):
        try:
            file = open(filename, "r")
            isError = True
            lineCount = 0
            oldState = ""
            voteList = []
            database1 = dict()
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


vt = ReadVotes()
vt.read_votes("data/votes.csv")
