import discord
import os
import random
import pprint
from functools import reduce

from keep_alive import keep_alive
# begin of character generation
species = ["Andorian", "Bajoran", "Betazoid", "Denobulan", "Human","Tellarite","Trill","Vulcan","Klingon","Klingon Augment"]

speciesAttributes = {
			"Andorian": {"daring":1, "control":1, "presence":1},
			"Bajoran": {"control":1, "daring":1, "insight":1},
			"Betazoid": {"insight":1, "presence":1, "reason":1 },
			"Denobulan": {"fitness":1, "insight":1, "reason":1 },
			"Tellarite": { "control":1, "fitness":1, "insight":1 },
			"Trill": {"control":1, "presence":1, "reason":1 },
			"Vulcan": {"control":1, "fitness":1, "reason":1 },
			"Klingon": {"daring":1, "fitness":1, "presence":1},
			"Klingon Augment": {"daring":2, "fitness":2, "presence":1 }
	            }
# Human attributes randomly choose 3 attributtes and add 1 to each

speciesTalents = { "Andorian":["Proud and Honorable","The Ushaan"],
                   "Bajoran":["Orb Experience", "Strong Pagh"],
		   "Betazoid":["Empath", "Telepath"],
		   "Denobulan":["Cultural Flexibility", "Parent Figure"],
		   "Human":["Resolute","Spirit of Discovery"],
		   "Tellarite":["Incisive Scrutiny", "Sturdy"],
		   "Trill":["Former Initiate", "Joined"],
		   "Vulcan":["Kolinahr", "Mind-meld", "Nerve Pinch"],
		   "Klingon":["To Battle","Brak'lul","R'uustai"],
		   "Klingon Augment":["5 Times Stronger", "Twice As Intelligent"]
                 }

organization = ["Starfleet","Klingon Defense Force"]

stera = ["Enterprise","Discovery","TOS","TMP","TNG","POSTDW"]

servicerank = [ "ensign", "ltjg", "lt", "ltcmdr", "cmdr", "capt" ]

attributes = { 'control':7, 'daring':7, 'fitness':7, 'insight':7, 'presence':7, 'reason':7 }

disciplines = {'command':1, 'conn':1, 'engineering':1, 'security':1, 'science':1, 'medicine':1 }

focuses = [ "Anthropology",
            "Astronaviation",
	    "Astrophysics",
	    "Botany",
	    "Composure",
	    "Computers",
    	    "Cybernetics",
	    "Diplomacy",
	    "Electro Plasma Power Systems",
	    "Emergency Medicine",
	    "Espionage",
	    "EVA",
	    "Evasive Action",
	    "Exo-tectonics",
	    "Genetics",
	    "Geology",
	    "Hand Phasers",
	    "Hand-to-Hand Combat",
	    "Helm Operations",
	    "Infectious Diseases",
	    "Infiltration",
	    "Interrogation",
	    "Linguistics",
	    "Persuaion",
	    "Philosophy",
	    "Physics",
	    "Psychiatry",
	    "Quantum Mechanics",
	    "Shipboard Tactical Systems",
	    "Small Craft",
	    "Spatial Phenomenon",
	    "Survival",
	    "Transporters and Replicators",
	    "Trauma Surgery",
	    "Virology",
	    "Warp Field Dynamics",
	    "Xenobiology"
          ]

commandTrackFocuses = [
			"Astronavigation",
			"Composure",
			"Diplomacy",
			"Extra-Vehicular Activity",
			"Evasive Action",
			"Helm Operations",
			"Inspiration",
			"Persuasion",
			"Small Craft",
			"Starship Recognition",
			"Starfleet Protocols",
			"Team Dynamics"
                      ]

operationsTrackFocuses = [
				"Computers",
				"Cybernetics",
				"Electro-Plasma Power Systems",
				"Espionage",
				"Hand Phasers",
				"Hand-to-Hand Combat",
				"Infiltration",
				"Interrogation",
				"Shipboard Tactical Systems",
				"Survival",
				"Transporters & Replicators",
				"Warp Field Dynamics"
                         ]

scienceTrackFocuses = [
			"Anthropology",
			"Astrophysics",
			"Botany",
			"Computers",
			"Cybernetics",
			"Emergency Medicine",
			"Exo-tectonics",
			"Genetics",
			"Geology",
			"Infectious Diseases",
			"Linguistics",
			"Physics",
			"Psychiatry",
			"Quantum Mechanics",
			"Trauma Surgery",
			"Virology",
			"Warp Field Dynamics",
			"Xenobiology"
                      ]

values = []
# user will input these statements.  Laster code will generate this or randomly pick from a file

traits = ["personal","equipment"]
# user will still have to input but this will give the categories of traits
# in the future this will be read from a file

talents = [
		("general", "Bold", None),
		("general", "Cautious", None),
		("general", "Collaboration", None),
		("general", "Constantly Watching", None),
		("general", "Dauntless", None),
		("general", "Personal Effects", "Main Character"),
		("general", "Studious", None),
	        ("general", "Technical Expertise", None),
	        ("general", "Tough", None),
		("command", "Advisor", "Command", 2),
		("command", "Defuse The Tension", "Command", 2),
		("command", "Follow My Lead", "Command", 3),
		("command", "Supervisor", "Main Character"),
		("conn", "Fly-by", "Conn", 2),
		("conn", "Precise Evasion", "Conn", 4),
		("conn", "Push The Limits", "Conn", 4),
		("conn", "Starship Expert", "Conn", 3),
		("security", "Close Protection", "Security", 4),
		("security", "Interrogation", "Security", 3),
		("security", "Mean Right Hook", None),
		("security", "Pack Tactics", None),
		("security", "Quick To Action", "Security", 3),
		("engineering", "A Little More Power", "Engineering", 3),
		("engineering", "I Know My Ship", "Engineering", 4),
		("engineering", "In The Nick Of Time", "Engineering", 3),
		("engineering", "In the Nick Of Time", "Science", 3),
		("engineering", "Intense Scrutiny", "Engineering", 3),
		("engineering", "Intense Scrutiny", "Science", 3),
		("engineering", "Jury-Rig", "Engineering", 4 ),
		("science", "Computer Expertise", "Science", 2),
		("science", "In The Nick Of Time", "Engineering", 3),
		("science", "In The Nick Of Time", "Science", 3),
		("science", "Intense Scrutiny", "Engineering", 3),
		("science", "Intense Scrutiny", "Science", 3),
		("science", "Testing A Theory", "Engineering", 2),
		("science", "Testing A Theory", "Science", 2),
		("medical", "Doctor's Orders", "Medicine", 4),
		("medical", "Field Medicine", None),
		("medical", "First Response", "Medicine", 3),
		("medical", "Quick Study", "Medicine", 3),
		("medical", "Triage", "Medicine", 3)
			
          ]

environment = [ "Homeworld", "Busy Colony", "Isolated Colony", "Frontier Colony", "Starship or Starbase", "Another Species World"]

upbringing = [ "Starfleet", "Business or Trade", "Agriculture or Rural", "Science and Technology", "Artistic and Creative", "Diplomacy and Politics"]

careerEvent =   [	"Ship Destroyed",
			"Death Of A Friend",
			"Lauded By Another Culture",
			"Negotiate A Treaty",
			"Required To Take Command",
			"Encounter With A Truly Alien Being",
			"Serious Injury",
			"Conflcit with a Hostile Culture",
			"Mentored",
			"Transporter Accident",
			"Dealing with a Plague",
			"Betrayed Ideals for A Superior",
			"Called Out A Superior",
			"New Battle Strategy",
			"Learns Unique Language",
			"Discovers an Artifact",
			"Special Commendation",
			"Solved An Engineering Crisis",
			"Breakthrough or Invention",
			"First Contact"
		]

officerRank = ["ensign","ltjg","lieutenant","lcdr","commander","captain"];

shipDepartments = ["co","xo","chief engineer","chief of security","chief medical officer","science officer","conn","navigator","counselor","communications aka ew officer","damage control"]

characterEra = None
characterOrganization = None
characterSpecies = None
characterSpeciesTrait = None
characterSpeciesTalents = []
characterTalents = []
characterAttributes = None;
characterFocuses = []
characterTalents = []
characterStress = None
characterDamageBonus = None
characterDepartment = None
characterRank = None
characterRole = None
characterEquipment = ["Communicator"]
characterEnvironment = None
humanAttributes = None
characterDisciplines = disciplines
characterUpbringing = None
characterAcceptUpbringing = None
characterAcademyTrack = None
characterCareer = None
characterCareerEvent = None
characterSheet = None

def stepOne():
	global characterEra
	global characterOrganization	
	global characterSpecies
	global characterSpeciesTrait
	global characterSpeciesTalents
	global characterTalents
	global characterAttributes
	global characterFocuses
	global characterTalents
	global characterStress
	global characterDamageBonus
	global characterDepartment
	global characterRank
	global characterRole
	global characterEquipment
	global characterEnvironment
	global humanAttributes
	global characterDisciplines
	global characterUpbringing
	global characterAcceptUpbringing
	global characterAcademyTrack
	global characterCareer
	global characterCareerEvent
	global characterSheet

	characterEra = None
	characterOrganization = None
	characterSpecies = None
	characterSpeciesTrait = None
	characterSpeciesTalents = []
	characterTalents = []
	characterAttributes = None;
	characterFocuses = []
	characterTalents = []
	characterStress = None
	characterDamageBonus = None
	characterDepartment = None
	characterRank = None
	characterRole = None
	characterEquipment = ["Communicator"]
	characterEnvironment = None
	humanAttributes = None
	characterDisciplines = disciplines
	characterUpbringing = None
	characterAcceptUpbringing = None
	characterAcademyTrack = None
	characterCareer = None
	characterCareerEvent = None
	characterSheet = None

	a = random.randint(0,len(species)-1) # choose species
	b = random.randint(0,1); # choose organization
	c = random.randint(0, len(stera) - 1) # choose era
	d = random.randint(0, len(talents) - 1) # choose talent

	#global characterEra
	characterEra = stera[ c ]
	#global characterSpecies
	characterSpecies = species[a]
	#global characterSpeciesTalents
	characterSpeciesTalents = speciesTalents[ species[a]]
	#global characterTalents
	characterTalents.append( talents[d] )
	#global speciesAttributes
	#global characterOrganization

	characterOrganization = organization[b]

	print( "ERA : ", characterEra )	
	print( "SPECIES TRAIT : ", characterSpecies )
	print( "SPECIES TALENTS : ",  characterSpeciesTalents)
	print( "INITIAL TALENT : " )
	pprint.pprint( characterTalents )
	print("OVERALL SPECIES ATTRIBUTES BEFORE : ", )
	pprint.pprint( speciesAttributes )
	print()

	e = random.sample(["control", "daring", "fitness", "insight", "presence", "reason"],3)
	f = { i:1 for i in e}

	speciesAttributes["Human"] = f

	print("OVERALL SPECIES  ATTRIBUTES AFTER  : ", )
	pprint.pprint( speciesAttributes )
	print()
	print()

	#global characterAttributes
	characterAttributes = attributes
	print("CURRENT SPECIES ATTRIBUTES : ", )
	pprint.pprint( speciesAttributes[ characterSpecies ] )
	print()
	print()

	print("CHARACTER ATTRIBUTES BEFORE : ", )
	pprint.pprint( characterAttributes )
	print()
	characterAttributes = {x:y+speciesAttributes[characterSpecies][x] if x in speciesAttributes[characterSpecies] else y for (x,y) in characterAttributes.items() }
	print("CHARACTER ATTRIBUTES AFTER : ", )
	pprint.pprint( characterAttributes )
	print()
	print()

def stepTwo():
	a = random.randint(0 ,len(environment) - 1)
	global characterEnvironment
	characterEnvironment = environment[a]
	print("ENVIRONMENT : ", characterEnvironment )
	print("PLAYER ADDS A VALUE BASED ON ENVIRONMENT")	
	print()
	#pprint.pprint( characterAttributes )
	#pprint.pprint( list(characterAttributes) )	

	#c = random.sample( list(characterAttributes), 1 )
	#d = random.sample( ["command","security","science"], 1 )

	global characterAttributes
	global characterDisciplines

	print("CHARACTER ATTRIBUTES BEFORE : ")
	pprint.pprint( characterAttributes )
	print()
	print("CHARACTER DISCIPLINES BEFORE : ")
	pprint.pprint( characterDisciplines )
	print()
	print()

	if a==0 : # homeworld
		print("PLAYER ADD VALUE BASED ON HOMEWORLD")
		print()
		a = random.sample( speciesAttributes[ characterSpecies ].keys(),1 )[0]
		characterAttributes[a]+=1
		b = random.sample(["command", "security", "science"],1)[0]
		characterDisciplines[b] += 1
	elif a==1 : # busy colony
		print("PLAYER ADD VALUE BASED ON BUSY COLONY")
		print()
		a = random.sample( ["daring","presence"], 1 )[0]
		b = random.sample( ["command", "security", "science"], 1)[0]
		characterAttributes[a]+=1
		characterDisciplines[b]+=1
	elif a==2 : # isolated colony
		print("PLAYER ADD VALUE BASED ON ISOLATED COLONY")
		print()
		a = random.sample( ["reason","insight"], 1 )[0]
		b = random.sample( ["engineering", "science", "medicine"], 1)[0]
		characterAttributes[a]+=1
		characterDisciplines[b]+=1
	elif a==3 : # frontier colony
		print("PLAYER ADD VALUE BASED ON FRONTIER COLONY")
		print()
		a = random.sample( ["control","fitness"], 1 )[0]
		b = random.sample( ["conn", "security", "medicine"], 1)[0]
		characterAttributes[a]+=1
		characterDisciplines[b]+=1
	elif a==4 : # starship or starbase
		print("PLAYER ADD VALUE BASED ON STARSHIP OR STARBASE")
		print()
		a = random.sample( ["control","fitness"], 1 )[0]
		b = random.sample( ["conn", "security", "medicine"], 1)[0]
		characterAttributes[a]+=1
		characterDisciplines[b]+=1
	elif a==5 : # another species' world
		print("PLAYER ADD VALUE BASED ON HOMEWORLD")
		print()
		notmyspecies = [i for i in species if i!=characterSpecies ]
		a = random.sample( notmyspecies, 1)[0]
		print("OTHER SPECIES HOMEWORLD : ", a)
		c = random.sample( list(speciesAttributes[a]), 1 )[0]
		b = random.sample( list(characterDisciplines), 1)[0]
		characterAttributes[c]+=1
		characterDisciplines[b]+=1
	else :
		print("ERROR")

	print("CHARACTER ATTRIBUTES AFTER : ")
	pprint.pprint( characterAttributes )
	print()
	print("CHARACTER DISCIPLINES AFTER : ")
	pprint.pprint( characterDisciplines )
	print()
	print()

def stepThree():
	a = random.randint(0,5) # upbringing
	b = random.randint(0,1) # 0 rebelled against upbringing,1 accepted upbringing

	global characterUpbringing
	characterUpbringing = upbringing[ a ]
	global characterAcceptUpbringing
	characterAcceptUpbringing = b
	print("CHARACTER UPBRINGING : ", characterUpbringing)
	if characterAcceptUpbringing==0 :
		print("CHARACTER REJECTS UPBRINGING")
	else :
 		print("CHARACTER ACCEPTS UPBRINGING")

	global characterTalents
	global chracterAttributes
	global characterDisciplines
	global characterFocuses

	print()
	print()
	print("CHARACTER ATTRIBUTES BEFORE : ")
	pprint.pprint(characterAttributes)
	print()
	print("CHARACTER DISCPLINES BEFORE : ")
	pprint.pprint(characterDisciplines)
	print()
	print()
	print("CHARACTER FOCUSES BEFORE : ")
	pprint.pprint( characterFocuses )
	print()
	print()
	print("CHARACTER TALENTS BEFORE : ")
	pprint.pprint( characterTalents )
	print()
	print()


	if a==0 : # Starfleet
		if characterAcceptUpbringing==0 :
			characterAttributes["daring"]+=2
			characterAttributes["insight"]+=1			
		else :
			characterAttributes["control"]+=2
			characterAttributes["fitness"]+=1

		c = random.sample( list(characterDisciplines), 1)[0]
		characterDisciplines[c]+=1
	
		characterTalents.append( random.sample( talents, 1 )[0] )

	elif a==1 : # Business or Trade
		if characterAcceptUpbringing==0 :
			characterAttributes["insight"]+=2
			characterAttributes["reason"]+=1
		else :
			characterAttributes["daring"]+=1
			characterAttributes["presence"]+=2

		c = random.sample( ["command", "engineering", "science"],1)[0]
		characterDisciplines[c]+=1

		characterTalents.append( random.sample( talents, 1 )[0] )

	elif a==2 : # Agriculture or Rural
		if characterAcceptUpbringing == 0 :
			characterAttributes["presence"]+=1
			characterAttributes["reason"]+=2
		else :
			characterAttributes["control"]+=1
			characterAttributes["fitness"]+=2

		c = random.sample(["conn","security","medicine"],1)[0]
		characterDisciplines[ c ] += 1

		characterTalents.append( random.sample( talents, 1 )[0] )
	elif a==3 : # Science and Technology
		if characterAcceptUpbringing == 0 :
			characterAttributes["daring"]+=1
			characterAttributes["insight"]+=2
		else :
			characterAttributes["control"]+=2
			characterAttributes["reason"]+=1

		c = random.sample(["conn","engineering","science","medicine"],1)[0]
		characterDisciplines[ c ] += 1

		characterTalents.append( random.sample( talents, 1 )[0] )
	elif a==4 : # Artistic and Creative
		if characterAcceptUpbringing == 0 :
			characterAttributes["daring"]+=1
			characterAttributes["fitness"]+=2
		else :
			characterAttributes["insight"]+=1
			characterAttributes["presence"]+=2

		c = random.sample(["command","engineering","science"],1)[0]
		characterDisciplines[ c ] += 1

		characterTalents.append( random.sample( talents, 1 )[0] )
	elif a==5 : # Diplomacy and Politics
		if characterAcceptUpbringing == 0 :
			characterAttributes["fitness"]+=1
			characterAttributes["reason"]+=2
		else :
			characterAttributes["control"]+=1
			characterAttributes["presence"]+=2

		c = random.sample(["command","conn","security"],1)[0]
		characterDisciplines[ c ] += 1

		characterTalents.append( random.sample( talents, 1 )[0] )
	else :
		print("ERROR")

	characterFocuses = random.sample( focuses, 1)

	print()
	print()
	print("CHARACTER ATTRIBUTES AFTER : ")
	pprint.pprint(characterAttributes)
	print()
	print("CHARACTER DISCPLINES AFTER : ")
	pprint.pprint(characterDisciplines)
	print()
	print()
	print("CHARACTER FOCUSES AFTER : ")
	pprint.pprint( characterFocuses )
	print()
	print()
	print("CHARACTER TALENTS AFTER : ")
	pprint.pprint( characterTalents )
	print()
	print()

def stepFour():
	global characterAcademyTrack
	characterAcademyTrack = random.sample(["Command","Operations","Sciences"],1)[0]

	global characterAttributes
	global characterDisciplines
	global characterFocuses
	global characterTalents

	print("CHARACTER ACADEMY TRACK : ", characterAcademyTrack)
	print()
	print("PLAYER WILL ADD VALUE BASED ON THIER TIME AT THE ACADEMY")
	print()
	print("CHARACTER ATTRIBUTES BEFORE : ")
	pprint.pprint( characterAttributes )
	print()
	print("CHARACTER DISCPLINES BEFORE : ")
	pprint.pprint( characterDisciplines )
	print()
	print("CHARACTER FOCUSES BEFORE : ")
	pprint.pprint( characterFocuses )
	print()
	print("CHARACTER TALENTS BEFORE : ")
	pprint.pprint( characterTalents )
	print()
	print()

	a = random.randint(2,3)
	print(a)
	print()
	if a==2 :
		b = random.sample(list(characterAttributes), 2)
		characterAttributes[ b[0] ] += 2
		characterAttributes[ b[1] ] += 1
	elif a==3 :
		b = random.sample(list(characterAttributes), 3)
		characterAttributes[ b[0] ] += 1
		characterAttributes[ b[1] ] += 1
		characterAttributes[ b[2] ] += 1

	pprint.pprint(b)
	print()

	
	if characterAcademyTrack=="Command" :
		c = random.sample(["command","conn"],1)[0]
		characterDisciplines[c]+=2

		if c=="Command" :
			d = random.sample(["conn","engineering","security","science","medicine"],2)
		else :
			d = random.sample(["command","engineering","security","science","medicine"],2)

		characterDisciplines[ d[0] ] += 1
		characterDisciplines[ d[1] ] += 1

		#characterFocuses = random.sample( commandTrackFocuses, 1)
		#characterFocuses.extend( random.sample([i for i in commandTrackFocuses if i!=characterFocuses[0]],2) )

		e = set(characterFocuses)
		f = set(commandTrackFocuses)
		g = f - e
		characterFocuses.extend( random.sample(g,1) )
		e = set(characterFocuses)
		f = set(focuses)
		g = f - e
		characterFocuses.extend( random.sample( g,2) )

		e = set(characterTalents)
		f = set(talents)
		g = f - e
		characterTalents.extend( random.sample( list(g), 1 ) )

		print()
	elif characterAcademyTrack=="Operations" :
		c = random.sample(["engineering","security"],1)[0]
		characterDisciplines[c]+=2

		d = random.sample( [i for i in list(disciplines) if i!=c] ,2)
		characterDisciplines[ d[0] ] += 1
		characterDisciplines[ d[0] ] += 1

		#characterFocuses = random.sample( operationsTrackFocuses, 1)
		#characterFocuses.extend( random.sample([i for i in operationsTrackFocuses if i!=characterFocuses[0]],2) )
		e = set(characterFocuses)
		f = set(operationsTrackFocuses)
		g = f - e
		characterFocuses.extend( random.sample(g,1) )
		e = set(characterFocuses)
		f = set(focuses)
		g = f - e
		characterFocuses.extend( random.sample( g,2) )


		e = set(characterTalents)
		f = set(talents)
		g = f - e
		characterTalents.extend( random.sample( list(g), 1 ) )

		print()
	elif characterAcademyTrack=="Sciences" :
		c = random.sample(["science","medicine"],1)[0]
		characterDisciplines[c]+=2

		d = random.sample( [i for i in list(disciplines) if i!=c] ,2)
		characterDisciplines[ d[0] ] += 1
		characterDisciplines[ d[0] ] += 1

		#characterFocuses = random.sample( scienceTrackFocuses, 1)
		#characterFocuses.extend( random.sample([i for i in scienceTrackFocuses if i!=characterFocuses[0]],2) )
		e = set(characterFocuses)
		f = set(scienceTrackFocuses)
		g = f - e
		characterFocuses.extend( random.sample(g,1) )
		e = set(characterFocuses)
		f = set(focuses)
		g = f - e
		characterFocuses.extend( random.sample( g,2) )


		e = set(characterTalents)
		f = set(talents)
		g = f - e
		characterTalents.extend( random.sample( list(g), 1 ) )

		print()

	print("CHARACTER ATTRIBUTES AFTER : ")
	pprint.pprint( characterAttributes )
	print()
	print("CHARACTER DISCPLINES AFTER : ")
	pprint.pprint( characterDisciplines )
	print()
	print("CHARACTER FOCUSES AFTER : ")
	pprint.pprint( characterFocuses )
	print()
	print("CHARACTER TALENTS AFTER : ")
	pprint.pprint( characterTalents )
	print()
	print()


def stepFive():
	print("PLAYER MUST ENTER A VALUE BASED ON OFFICER TYPE")
	a = random.randint(0,2) # 0 is young officer, 1 is experienced officer, 2 is veteran officer
	global characterCareer
	global characterTalents
	global characterRank

	print("CHARACTER TALENTS BEFORE : ")
	pprint.pprint(characterTalents)
	print()
	print()

	if a==0 :
		characterCareer = "Young Officer"
		characterTalents.append( tuple(["general","Untapped Potential", None]) )
		characterRank = random.sample(["ensign","ltjg"],1)[0]
	elif a==1 : 
		characterCareer = "Experienced Officer"
		e = set(characterTalents)
		f = set(talents)
		g = f - e
		characterTalents.append( random.sample( list(g), 1)[0] )
		characterRank = random.sample(["lieutenant","lcdr"],1)[0] 
	elif a==2 :
		characterCareer = "Veteran Officer"
		characterTalents.append( tuple(["general","Veteran", None]) )
		characterRank = random.sample(["commander","captain"],1)[0]
	print()

	print("CHARACER TALENTS AFTER : ")
	pprint.pprint(characterTalents)
	print()
	print()

def stepSix():
	a = random.randint(0,19)
	global characterCareerEvent
	global characterAttributes
	global characterDiscplines
	global characterFocuses

	characterCareerEvent = careerEvent[ a ]
	print("CHARACTER CAREER EVENT : ", characterCareerEvent )
	print()
	print()
	print("CHARACTER ATTRIBUTES BEFORE : ")
	pprint.pprint( characterAttributes )
	print()
	print("CHARACTER DISCPLINES BEFORE : ")
	pprint.pprint( characterDisciplines )
	print()
	print("CHARACTER FOCUSES BEFORE : ")
	pprint.pprint( characterFocuses )
	print()

	if a==0 :
		characterAttributes["daring"]+=1
		characterDisciplines["security"]+=1
		print()
	elif a==1 :
		characterAttributes["insight"]+=1
		characterDisciplines["medicine"]+=1
		print()
	elif a==2 :
		print("ENTER A CHARACTER TRAIT RELATED TO LAUDED BY ANOTHER CULTURE")
		characterAttributes["presence"]+=1
		characterDisciplines["science"]+=1
		print()
	elif a==3 :
		characterAttributes["control"]+=1
		characterDisciplines["command"]+=1
		print()
	elif a==4 :
		characterAttributes["daring"]+=1
		characterDisciplines["command"]+=1
		print()
	elif a==5 :
		characterAttributes["reason"]+=1
		characterDisciplines["science"]+=1
		print()
	elif a==6 :
		print("ENTER A CHARACTER TRAIT RELATED TO SERIOUS INJURY")
		characterAttributes["fitness"]+=1
		characterDisciplines["medicine"]+=1
		print()
	elif a==7 :
		characterAttributes["fitness"]+=1
		characterDisciplines["security"]+=1
		print()
	elif a==8 :
		i = random.sample( list(characterAttributes), 1)[0]
		characterAttributes[ i ] += 1
		characterDisciplines["conn"]+=1
		print()
	elif a==9 :
		characterAttributes["control"]+=1
		characterDisciplines["conn"]+=1
		print()
	elif a==10 :
		characterAttributes["insight"]+=1
		characterDisciplines["medicine"]+=1
		print()
	elif a==11 :
		characterAttributes["presence"]+=1
		characterDisciplines["command"]+=1
		print()
	elif a==12 :
		characterAttributes["reason"]+=1
		characterDisciplines["conn"]+=1
		print()
	elif a==13 :
		characterAttributes["daring"]+=1
		characterDisciplines["security"]+=1
		print()
	elif a==14 :
		characterAttributes["insight"]+=1
		characterDisciplines["science"]+=1
		print()
	elif a==15 :
		characterAttributes["reason"]+=1
		characterDisciplines["engineering"]+=1
		print()
	elif a==16 :
		characterAttributes["fitness"]+=1
		i = random.sample( list(characterDisciplines), 1)[0]
		characterDisciplines[ i ]+=1
		print()
	elif a==17 :
		characterAttributes["control"]+=1
		characterDisciplines["engineering"]+=1
		print()
	elif a==18 :
		i = random.sample( list(characterAttributes), 1 )[0]
		characterAttributes[ i ]+=1
		characterDisciplines["engineering"]+=1
		print()
	elif a==19 :
		characterAttributes["presence"]+=1
		i = random.sample( list(characterDisciplines), 1)[0]
		characterDisciplines[ i ]+=1
		print()

	b = set(focuses)
	c = set(characterFocuses)
	d = b - c
	characterFocuses.extend( random.sample( d, 2 ) )

	print()

	print()
	print()
	print("CHARACTER ATTRIBUTES AFTER : ")
	pprint.pprint( characterAttributes )
	print()
	print("CHARACTER DISCPLINES AFTER : ")
	pprint.pprint( characterDisciplines )
	print()
	print("CHARACTER FOCUSES AFTER : ")
	pprint.pprint( characterFocuses )
	print()

def stepSeven():
	print("PLAYER TO ENTER ONE FINAL VALUE")
	print()
	global characterStress
	global characterDamageBonus

	characterStress = characterAttributes["fitness"] + characterDisciplines["security"]

	setCharacterDepartment()
	checkAttributes()
	checkDisciplines()

	characterStress = characterAttributes["fitness"] + characterDisciplines["security"]
	characterDamageBonus = characterDisciplines["security"]

	printCharacter()

def setCharacterDepartment():
	print()
	global characterDepartment

def checkAttributes():
	a = reduce( lambda x,y: x+y, list(characterAttributes.values()))
	print("CHARACTER ATTRIBUTES CHECK : ", a)
	pprint.pprint( characterAttributes )
	print("CHARACTER TALENTS : ")
	pprint.pprint( characterTalents )
	print()
	print()

	b = set(characterTalents)
	c = set([ tuple(["general","Untapped Potential",None])] )
	#pprint.pprint(c)
	d = len(b&c)
	if d==0 :
		maxAttributeValue = 12
	else :
		maxAttributeValue = 11

	print("CHARACTER MAX ATTRIBUTE VALUE : ", maxAttributeValue)	
	print()
	balanceAttributes(maxAttributeValue)
	a = reduce( lambda x,y: x+y, list(characterAttributes.values()))
	print("CHARACTER ATTRIBUTES TOTAL FINAL : ", a)
	print()
	print()

def balanceAttributes(n):
	global characterAttributes

	i = 0
	print("CHARACTER ATTRIBUTES TO BALANCE : ")
	pprint.pprint(characterAttributes)
	print()
	print()

	for (a,b) in characterAttributes.items():
		if b>n :
			characterAttributes[a] = n - 1

	print("CHARACTER ATTRIBUTES AFTER INITIAL BALANCE : ")
	pprint.pprint( characterAttributes )
	print()
	print()
	print("ATTRIBUTE POINTS TO ASSIGN : ", i)
	print()
	print()

	c = [i for (i,j) in characterAttributes.items() if j<n ]
	print("CHARACTER ATTRIBUTES AFTER FINAL INCREASE : ")
	pprint.pprint(c)
	random.shuffle(c)
	pprint.pprint(c)
	characterAttributes[ c[0] ] += 1
	characterAttributes[ c[1] ] += 1
	pprint.pprint( characterAttributes )
	print()
	print()

def checkDisciplines():
	a = reduce( lambda x,y: x+y, list(characterDisciplines.values()))
	print("CHARACTER DISCPLINES CHECK : ", a)
	pprint.pprint( characterDisciplines )
	print()

	b = set(characterTalents)
	c = set([ tuple(["general","Untapped Potential",None])] )
	#pprint.pprint(c)
	d = len(b&c)
	if d==0 :
		maxDisciplineValue = 5 
	else :
		maxDisciplineValue = 4

	print("CHARACTER MAX DISCIPLINE VALUE : ", maxDisciplineValue)
	balanceDisciplines( maxDisciplineValue )
	a = reduce( lambda x,y: x+y, list(characterDisciplines.values()))
	print("CHARACTER DISCPLINES TOTAL FINAL : ",a)
	print()
	print()

def balanceDisciplines( n ):
	print()
	global characterDiscplines
	i = 0
	print("CHARACTER DISCIPLINES TO BALANCE : ")
	pprint.pprint(characterDisciplines)
	print()
	print()

	for (a,b) in characterDisciplines.items():
		if b>n :
			characterDisciplines[a] = n - 1

	print("CHARACTER DISCIPLINES AFTER INITIAL BALANCE : ")
	pprint.pprint( characterDisciplines )
	print()
	print()
	print("DISCPLINE POINTS TO ASSIGN : ",i)
	print()
	print()
	c = [i for (i,j) in characterDisciplines.items() if j<n ]
	print("CHARACTER DISCIPLINES AFTER FINAL INCREASE : ")
	pprint.pprint(c)
	random.shuffle(c)
	pprint.pprint(c)
	characterDisciplines[ c[0] ] += 1
	characterDisciplines[ c[1] ] += 1
	pprint.pprint( characterDisciplines )
	print()
	print()

def printCharacter():
	print("CHARACTER")
	print("CHARACTER SPECIES : ", characterSpecies)
	print("CHARACTER SPECIES TALENTS : ")
	pprint.pprint(characterSpeciesTalents)
	print("NAME : <YOU WILL INSERT HERE>")
	print("ERA : ", characterEra)
	print("ORGANIZATION : ", characterOrganization )
	print("RANK : ", characterRank)
	print("CHARACTER ACADEMY TRACK : ", characterAcademyTrack)
	print("CHARACTER STRESS : ", characterStress )
	print("CHARACTER BONUS DAMAGE : ", characterDamageBonus )
	print("ENTER AT LEAST 4 VALUES")
	print("ENTER AT LEAST 4 TRAITS")
	print()
	print("CHARACTER ATTRIBUTES : ")
	pprint.pprint(characterAttributes)
	print()
	print("CHARACTER DISCIPLINES : ")
	pprint.pprint(characterDisciplines)
	print()
	print("CHARACTER TALENTS : " )
	pprint.pprint( characterTalents )
	print()
	print("CHARACTER FOCUSES : " )
	pprint.pprint( characterFocuses )
	print()
	print()
	print()
	print()

	result = "CHARACTER\n\n"
	result += "CHARACTER SPECIES : " + characterSpecies + "\n\n"
	result += "CHARACTER SPECIES TALENTS : \n" + pprint.pformat(characterTalents) + "\n\n"
	result += "NAME : <YOU WILL INSERT HERE>\n\n"
	result += "ERA : " + characterEra + "\n\n"
	result += "ORGANIZATION : " + characterOrganization + "\n\n"
	result += "RANK : " + characterRank + "\n\n"
	result += "CHARACTER ACADEMY TRACK : " + characterAcademyTrack + "\n\n"
	result += "CHARACTER STRESS : " + pprint.pformat(characterStress) + "\n\n"
	result += "CHARACTER BONUS DAMAGE : " + pprint.pformat(characterDamageBonus) + "\n\n"
	result += "ENTER AT LEAST 4 VALUES AND 4 TRAITS\n\n"
	result += "CHARACTER ATTRIBUTES : \n" + pprint.pformat(characterAttributes) + "\n\n"
	result += "CHARACTER DISCIPLINES : \n" + pprint.pformat(characterDisciplines) + "\n\n"
	result += "CHARACTER TALENTS : \n" + pprint.pformat(characterTalents) + "\n\n"
	result += "CHARACTER FOCUSES : \n" + pprint.pformat(characterFocuses) + "\n\n\n\n"


	print("CHARACTER AS SINGLE STRING : ")
	print(result)
	global characterSheet
	characterSheet = result

def main():
	print("hello world")
	print()
	print()
	print("SPECIES")
	print("NAME")
	print("ORGANIZATION")
	print("RANK")
	print("SPECIES TRAIT")
	print("TRAITS")	
	print("VALUES")
	print("DISCIPLINES")
	print("FOCUSES")
	print("TALENTS")
	print()
	print()

	print("STEP ONE")
	stepOne()

	print("STEP TWO")
	stepTwo()

	print("STEP THREE")
	stepThree()

	print("STEP FOUR")
	stepFour()

	print("STEP FIVE")
	stepFive()

	print("STEP SIX")
	stepSix()

	print("STEP SEVEN")
	stepSeven()
# end of character generation


client = discord.Client()

@client.event
async def on_ready():
    print("I'm in")
    print(client.user)

@client.event
async def on_message(message):
    if message.author != client.user:
        #await client.send_message(message.channel, message.content[::-1])

        if message.content=="!gen":
          message.content = "making character..."
          await client.send_message(message.channel, message.content )
          main()

          #message.content="CHARACTER\n"
          #message.content+="NAME: <YOU WILL INSERT HERE>\n"
          #message.content+="ERA : " + characterEra + "\n"
          message.content = characterSheet


          await client.send_message(message.channel,message.content)
          
        
keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)

