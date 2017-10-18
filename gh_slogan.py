# gh_slogan.py
# 2017, polarysekt


from random import randint

#g_ghSloganList = [ "DEFAULT SLOGAN", "It's a secret to everyone.", "CTOR BLOGGEN", "Welcome Back" ]

g_ghSloganList = [ """ “Live as if you were to die tomorrow. Learn as if you were to live forever” ― Mahatma Gandhi """,
""" “Without music, life would be a mistake” ― Friedrich Nietzsche """,
""" “Insanity is doing the same thing, over and over again, but expecting different results” ― Narcotics Anonymous """,
""" “All that we see or seem is but a dream within a dream” ― Edgar Allan Poe """,
""" “Learning never exhausts the mind” ― Leonardo da Vinci """,
""" “The supreme art of war is to subdue the enemy without fighting” ― Sun Tzu """,
""" “Not all those who wander are lost” ― J.R.R. Tolkien """,
""" “I have not failed. I've just found 10,000 ways that won't work” ― Thomas Edison """,
""" “If opportunity doesn't knock, build a door” ― Milton Berle """,
""" “The secret of getting ahead is getting started” ― Mark Twain """,
""" “The only true wisdom is in knowing you know nothing” ― Socrates """,
""" “Everything has beauty, but not everyone sees it” ― Confucious """,
""" “It is during our darkest moments we must focus to see the light” ― Aristotle """
]

def getSlogan():
    return g_ghSloganList[randint(0,len(g_ghSloganList)-1)]

def test_units():
    
    print( getSlogan() )
    return True


def main():
    test_units()

if __name__ == "__main__":
    main()
