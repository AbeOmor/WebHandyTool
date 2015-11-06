"""
@author Eric Le Fort
"""
class Parser():
    
    """
     Searches through a String for a certain phrase or term. Returns the starting index for all occurrences of the query String.
     If the query is not located, it will return an empty array.
     @param query - The String we are looking for.
     @param data - The String we are searching through.
     @return Indexes corresponding to the beginning of the location of the String in question.
    """
    def searchForString(query, data):
        locations = [];
        queryIndex = 0;
        
        data.strip();
        query.strip();
        query = query.lower();
        data = data.lower();
        
                                                    # Impossible for data to contain query or query is nonsensical.
        if len(query) > len(data) or (len(query) == len(data) and not query is data) or len(query) == 0: 
            return [];
        
        for i in range(0, len(data)):
            if data[i] == query[queryIndex]:        # Current location is matching the query pattern so far.
                if queryIndex == len(query) - 1:    # The whole query pattern is matched, add starting index.
                    locations.append(i - len(query) + 1);
                    queryIndex = 0;
                else:
                    queryIndex += 1;
                
            else:                                   #Current location didn't match the pattern.
                if data[i] == query[0]:
                    queryIndex = 1;
                else:
                    queryIndex = 0;   
                
        return locations;
    
    """
    Searches through a String for a certain phrase or term. Returns results that are close to the query as well.
     (i.e. "ap ple" or "bpple" would be noted for "apple") Returns the starting index for all occurrences of Strings sufficiently close to
     the query. If the query is not located, it will return an empty array.
     @param query - The String we are looking for.
     @param data - The String we are searching through.
     @param distance - The size of the acceptable variation from the query.
     @return Indexes corresponding to the beginning of the location of the String in question.
    """
    def searchForSimilarString(query, data, proximity):
        locations = [];
        queryIndex = 0;
        distance = 0;
        
        data.strip();
        query.strip();
        query = query.lower();
        data = data.lower();
        
        if len(query) > len(data) or (len(query) == len(data) and not query is data) or len(query) == 0 or proximity > (0.4) * len(query):
            return [];
        
        for i in range(0, len(data)):
            if data[i] == query[queryIndex]:
                if queryIndex == len(query) - 1:
                    locations.append(i - len(query) + 1);
                    queryIndex = 0;
                    distance = 0;
                else:
                    queryIndex += 1;
            elif distance < proximity:
                if queryIndex == len(query) - 1:
                    locations.append(i - len(query) + 1);
                    queryIndex = 0;
                    distance = 0;
                elif isWhitespace(data[i]):
                    distance += 1;
                else:
                    distance += 1;
                    queryIndex += 1;
            else:
                if data[i] == query[0]:
                    queryIndex = 0;
                    distance = 0;
                else:
                    queryIndex = 0;
                    distance = 0;

        return locations;

    """
     Returns true if the character passed in is a whitespace character such as tab, space or newline.
     @param a - The character to be checked.
     @return Whether the character is whitespace.
    """
    def isWhitespace(a):
        return a == ' ' or a == '    ' or a == os.linesep;