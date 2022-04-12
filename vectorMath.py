import math


# Calculates the magnitude between two vectors / kalkulerer avstanden mellom to vektorer

vec1 = (1, 1)
vec2 = (3, 3)

def magnitude(vec1,vec2):

    


    x1 = vec1[0]
    x2 = vec2[0]
    y1 = vec1[1]
    y2 = vec2[1]


    return     math.sqrt(   (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1)    )    




# Sinus og Cosinus
def sine(hyp,opp):
    # sine = Opposite/Hyp
    print(opp/hyp)
    return opp/hyp


def cosine(hyp,adj):
    # cosine = adjacent/Hyp
    print(adj/hyp)
    return adj/hyp




# Kalkulerer retningen mellom to vektorer 
vec1 = (1,1)
vec2 = (1,5)

def calculateDirection(v1,v2):

    c = magnitude(vec1,vec2)
    x1 = v1[0]
    x2 = v2[0]
    y1 = v1[1]
    y2 = v2[1]

    a = x2-x1
    b=  y2-y1

    #print(a,b,c)

    angle = math.atan2(b,a)
    angle = convertToDegrees(angle)
    return angle

def calculateDirectionInRadians(v1,v2):

    c = magnitude(vec1,vec2)
    x1 = v1[0]
    x2 = v2[0]
    y1 = v1[1]
    y2 = v2[1]

    a = x2-x1
    b=  y2-y1

    #print(a,b,c)

    angle = math.atan2(b,a)
    return angle

def convertToDegrees(angle):

    return (angle/math.pi) *180




#calculateDirection(vec1,vec2)


#math.atan2()

#poseidoncoder70
