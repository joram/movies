import gevent
import django
django.setup()

from tasks.base import BaseTask
from apps.movies.models.movie import Movie

BAD_FILENAMES = [
  "Akira p1.ogm",
  "Akira p2.ogm",
  "Batman 1966",
  "Batman1989",
  "El Capitan Fred Padula 1971"
]

FULL_BAD_FILENAMES = ['Akira p1.ogm', 'Akira p2.ogm', 'Batman 1966', 'Batman1989', 'El Capitan Fred Padula 1971', u'Fern Gully The Last Rainforest', u'Flash Gordon 1980', u'Howls Moving Castle', u'Indiana Jones and The Last Crusade', u'Indiana Jones Temple of Doom', u'Indiana Jones The Last Crusade', u'It Follows 2014', u'Jurassic.Park[1993]DvDrip-aXXo', u'Jurassic.Park.III[2001]DvDrip-aXXo', u'Justin and the Knights of Valor', u"KIki's Delivery Serivice", u'Kikis Delivery Service', u'Law Abiding Citizen.flv', u'Lucas in love.mov', u'Mad Max Beyond Thunderdome', u'Mad Max Thunderdome', u'Maleficent.2014.1080p.BluRay.x264.YIFY', u'movies.txt', u'Much Ado About Nothing 2012', u'My Neighbors the Yamadas', u'Nausica\xe4 of the Valley of the Wind', u'Pokemon.AVI', u'ponyo on the cliff by the sea', u'Porco Rosso', u'Reel Rock 2010', u'Reel Rock 2011.mov', u'Reel Rock 2012 DVD', u'Reel Rock 2013.mov', u'Rise of the Guardians', u'Saints Young Men', u'Sherlock Holmes', u'SNL Best of Christopher Walken', u'Stardust.wmv', u'The Amazing Spiderman', u'The Cat Returns', u'The Fantasia Legacy: The Concert Feature', u'The Fantastic Four - The Movie', u'The Hobbit 1977', u'The Hobbit The Battle of the Five Armies 2014 DVDSCR XviD-MAXSPEED www.torentz.3xforum.ro', u'The Hunger Games 01', u'The Hunger Games 02 Catching Fire', u'The Hunger Games 03 Mockingjay Part 1', u'The Incredibles', u'The Legend of Bagger Vance D1', u'The Legend of Bagger Vance D2', u'the secret world of arrietty', u'The Simpsons Movie.mpg', u'The Thing 1982', u'The Time Travelers Wife.m4v', u'They.Live.1988', u'Thumbs.db', u'Tinker Tailor Soldier Spy', u'Tomb Raider The Cradle Of Life', u'Tonari.no.Totoro', u'Undertaking Betty - Plots with a view', u'[UsaBit.com] -fr .hill.2011.brrip.xvid ocw', u'Whisper of the Heart', u'101 Dalmations', u'102 Dalmatians', u'A Bugs Life', u'A Knights Tale', u'A Long Way Down', u'A Scanner Darkly', u'A little princess', u'Aladdin and the King of Thieves ', u'Aladdin', u'Alice In Wonderland', u'An American In Paris', u'Anastasia', u'Anchors Aweigh', u'Army of Darkness', u'Arsenic and Old Lace', u'Astro Boy', u'Atlantis The Lost Empire', u'Aviator', u'Back to the Future 1', u'Back to the Future 2', u'Back to the Future 3', u'Balls of Fury', u'Basilisk The Serpent King', u'Batman & Robin1997', u'Batman 1989', u'Batman - City Of Scars', u'Batman Begins 2005', u'Batman Gotham Knight', u'Batman Mask of the Phantasm', u'Batman Returns', u'Batman The Dark Knight 2008', u'Batteries not Included', u'Beauty and the Beast', u'Bedknobs and Broomsticks', u'Beowulf', u'Big Hero 6', u'Bill And Teds Excellent Adventure', u'Black Book', u'Blade 1', u'Blade 2', u'Blade 3', u'Blade Runner', u'Bolt', u'Brave', u'Bride And Prejudice', u'Brigadoon', u'Bringing up Baby', u'Buffalo Soldiers', u'Calvary', u'Captain America 2 The Winter Soldier', u'Captain America The First Avenger ', u'Captain Kronos Vampire Hunter', u'Cars', u'Casablanca', u'Cats', u'Catwoman ', u'Chicago', u'Chicken Run', u'Cinderella', u'Close Encounters of the Third Kind', u'Clue', u'Clueless', u'Congo', u'Contagion', u'Cool Runnings', u'Cowboys and Aliens', u'Darby OGill and the Little People', u'Daredevil', u'Deathtrap', u'Despicable Me 2', u'Despicable Me', u'Die Hard', u'District 9', u'Doctor Strange - The Sorcerer Supreme', u'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb', u'Drive', u'Duck Soup 1933', u'Earth Girls Are Easy', u'Easy A', u'Elektra', u'Elephants Dream', u'Enchanted', u'Enders Game', u'Entrapment', u'Epic', u'Escape from Planet Earth', u'Event Horizon', u'Fantasia 2000', u'Fantasia', u'Fantastic Four', u'Fantastic Mr Fox', u'Fear and Loathing in Las Vegas', u'Field of Dreams', u'Finding Nemo', u'Flash Gordon', u'Flashdance', u'Forbidden Planet', u'Forgetting Sarah Marshall', u'Fritz The Cat', u'Frozen', u'Futurama Benders Big Score', u'Futurama Benders Game', u'Futurama The Beast With A Billion Backs', u'Futurama - Into The Wild Green Yonder', u'Gambit', u'Garfield A tail of two kitties', u'Gentlemans Agreement', u'Gentlemen Prefer Blondes', u'Ghost in the Shell 2', u'Ghostbusters', u'Gnomeo and Juliet', u'Gone in 60 Seconds', u'Grave of the Fireflies', u'Green Lantern', u'Guardians of the Galaxy', u'Halo legends', u'Harry Potter 1 Philosophers Stone', u'Harry Potter 2 The Chamber of Secrets', u'Harry Potter 3 Prisoner of Azkaban', u'Harry Potter 4 Goblet of Fire', u'Harry Potter 5 Order of the Phoenix', u'Harry Potter 7 Deathly Hallows Part 1', u'Harry Potter 7 Deathly Hallows Part 2', u'Harry Potter and the Half Blood Prince', u'Hello Dolly', u'Hercules', u'High Society', u'Home', u'Hoodwinked', u'Hop', u'Horton Hears a Who', u'Hot Fuzz', u'House of Flying Daggers', u'Hulk vs Thor', u'Hulk vs Wolverine', u'I Am Legend', u'I Know That Voice', u'I Robot', u'Ice Age 3 Dawn Of The Dinosaurs', u'Importance of Being Earnest', u'Inception', u'Independence Day', u'Indiana Jones and the Last Crusade', u'Indiana Jones and the Raiders of the Lost Ark', u'Indiana Jones and the Temple of Doom', u'Iron Man 2', u'Iron Man 3', u'Iron Man and Captain America Heroes United', u'Iron Man', u'Iron Sky', u'James Bond Dr', u'James Bond From Russia with Love', u'James Bond Goldfinger', u'James Bond On Her Majestys Secret Service', u'James Bond Thunderball', u'James Bond You Only Live Twice', u'Jesus Christ Superstar', u'Jonah Hex', u'Julie and Julia', u'Jurassic Park 2 The Lost World', u'Justice League Crisis on Two Earths', u'Karate Kid', u'KickAss', u"Kiki's Delivery Service", u'Killer Bean Forever', u'Kiss Me Kate 1953', u'Kung Fu Panda', u'Lady And The Tramp', u'Laputa Castle in the Sky', u'Legend of the Guardians', u'Lego Star Wars The Empire Strikes Out', u'Lilo and Stitch', u'Live Free or Die Hard', u'Logorama', u'Looper 2012', u'Lord of the Rings 1 The Fellowship of the Ring', u'Lord of the Rings 2 The Two Towers', u'Lord of the Rings 3 The Return of the King', u'Mad Max 1', u'Mad Max 2: The Road Warrior', u'Mad Max 3: Beyond Thunderdome', u'Man of Steel 2013', u'Margin Call', u'Mark of Zorro', u'Mash the Movie', u'Mask of Zorro', u'Mass Effect Paragon Lost', u'Master and Commander', u'Mean Girls', u'Meet The Robinsons', u'Megamind', u'Memento', u'Men In Black', u'Meru', u'Midnight in Paris', u'Midnight in the Garden of Good and Evil', u'Moneyball', u'Monkey Bone', u'Monsters Inc', u'Monsters University', u'Monsters Vs Aliens', u'Moon', u'Moulin Rouge', u'Mr and Mrs Smith', u'Mr', u'Much Ado About Nothing', u'Mulan 2', u'Mulan', u'Muppet Treasure Island', u'Muppets Most Wanted', u'My Fair Lady', u'My Little Pony Equestria Girls- Rainbow Rocks', u'My Little Pony Equestria Girls', u'My Neighbour Totoro', u'Mystery Men', u'National Treasure Book of Secrets', u'Nausicaa of the Valley of the Wind', u'Neko no Ongaeshi', u'Newsies', u'Nims Island', u'Oceans 11', u'Oceans 12', u'Oceans 13', u'Office Space', u'Oliver and Company', u'Only Yesterday', u'Outbreak', u'Pacific Rim', u'Panda! Go Panda!', u'Paper Man', u'Paperman', u'Paprika', u'Paranormal Activity', u'Philomena', u'Pirates Of The Caribbean 1 The Curse Of The Black Pearl', u'Pirates Of The Caribbean 2 Dead Mans Chest', u'Pirates Of The Caribbean 3 At Worlds End', u'Pirates Of The Caribbean 4 On Stranger Tides ', u'Pitch Black', u'Planet Of The Apes 2001', u'Planet Of The Apes', u'Pocahontas', u'Ponyo', u'Pride and Prejudice', u'Prince of Persia', u'Princess mononoke', u'Pulp Fiction', u'Puss in Boots', u'Quest for Camelot', u'Rango', u'Ratatouille', u'Red 2', u'Red', u'Reel Rock 10', u'Repo! the Genetic Opera', u'Requiem For A Dream', u'Reservoir Dogs', u'Rio', u'Rise of the Planet of the Apes', u'Robbie The Reindeer In Hooves Of Fire', u'Robbie The Reindeer In Legend Of The Lost Tribe', u'Robin Hood 1973', u'Robin Hood 2010', u'Robin Hood Men In Tights', u'Roman Holiday', u'Rosencrantz and Guildenstern are Dead', u'Saw', u'Scott Pilgrim vs the World', u'Searching for Bobby Fischer', u'Sense And Sensibility 1995', u'Serenity', u'Seven Samurai', u'Shall We Dance', u'Shark Tale', u'Sherlock Holmes 2009', u'Sherlock Holmes A Game of Shadows', u'Shrek 2', u'Shrek the Third', u'Shrek', u'Sinbad And The Minotaur', u"Singin' in the Rain", u'Sleeping Beauty', u'Sneakers', u'Snow White and the Seven Dwarfs', u'Source Code', u'Space Jam', u'Space Pirate Captain Harlock', u'Spanish', u'Spartacus', u'Spawn', u'Speed', u'Spiderman 2', u'Spiderman', u'Spirited Away', u'Star Trek 2009', u'Star Trek 2 the Wrath of Khan', u'Star Trek 5 the Final Frontier', u'Stargate SG1 Children of the Gods', u'Starship Troopers', u'Steamboy', u'Stranger Than Fiction', u'Super 8', u'Superman & Batman Public Enemies', u'Superman Batman Apocalypse', u'Superman', u'Taken 2', u'Taken', u'Tales from Earthsea', u'Tangled', u'Tenacious D', u'Terminator 3 Rise of the Machines', u'Terminator Judgement Day', u'Terminator Salvation', u'Terminator', u'Thank You for Smoking', u'The ATeam', u'The Adjustment Bureau', u'The Adventures of Priscilla Queen of the Desert 1994', u'The Adventures of Tintin', u'The Aristocats', u'The Artist', u'The Avengers', u'The Backup Plan', u'The Big Lebowski', u'The Birdcage', u'The Birds', u'The Book of Life', u'The Borrower Arrietty', u'The Cabin in the Woods', u'The Chosen One', u'The Chronicles Of Riddick Dark Fury', u'The Chronicles Of Riddick', u'The Chronicles of Narnia Prince Caspian', u'The City of Lost Children', u'The Court Jester', u'The Covenant 2', u'The Croods', u'The Curse of the Midas Box', u'The Dark Knight Rises', u'The Day The Earth Stood Still 2008', u"The Emperor's New Groove", u'The Exorcist', u'The Expendables 2 ', u'The Expendables', u'The Fifth Element', u'The Girl With A Dragon Tattoo ', u'The Gods Must Be Crazy II', u'The Gods Must Be Crazy', u'The Golden Compass', u'The Graduate', u'The Grand Budapest Hotel', u'The Great Gatsby 2013', u'The Great Mouse Detective', u'The Green Hornet', u'The Green Lantern', u'The Hobbit - An Unexpected Journey', u'The Hunchback of Notre Dame 2', u'The Hunchback of Notre Dame', u'The INcredible Hulk', u'The Illusionist', u'The Innocents', u'The Italian Job 1969', u'The Italian Job 2003', u'The Jane Austen Book Club', u'The Last Starfighter', u'The Lego Movie', u'The Librarian 2 Return to king Solomons Mines', u'The Librarian 3 The Curse of the Judas Chalice', u'The Librarian: Quest for the Spear', u'The Lion King 2', u'The Lion King', u'The Little Mermaid', u'The Lord of the Rings 1978', u'The Matrix Reloaded', u'The Matrix Revolutions', u'The Matrix', u'The Muppet Christmas Carol', u'The Music Man', u'The Net 2', u'The Neverending Story', u'The Nightmare Before Christmas', u'The People vs Larry Flynt', u'The Perfect Game', u'The Pirates! In An Adventure With Scientists!', u'The Prestige', u'The Prince of Egypt', u'The Princess Bride', u'The Princess and the Frog', u'The Punisher', u'The Rescuers Down Under', u'The Rescuers', u'The Road to El Dorado', u'The Secret Garden', u'The Secret of Kells 2009', u'The Smurfs', u'The Social Network', u'The Sorcerers Apprentice', u'The Sting', u'The Sum of All Fears', u'The Swan Princess', u'The Unsinkable Molly Brown', u'The Whole Nine Yards', u'The Wiz', u'The Wolf Of Wall Street', u'They Live 1988', u'Thick As Thieves', u'This Is Spinal Tap', u'Thor 2 The Dark World', u'Thor', u'Timeline', u'To Catch a Thief', u'Tomb Raider The Cradle of Life', u'Tomb Raider', u'Touching the Void 2003', u'Toy Story 2', u'Toy Story 3', u'Toy Story', u'Trainspotting', u'Transformers 3 Dark of the Moon ', u'Treasure Planet', u'Troll Hunter', u'Truckers', u'Turbo', u'Unstoppable', u'Unthinkable', u'Up', u'Victor Victoria', u'WALL-E', u'Waiting', u'Waking Ned Devine', u'Wallace And Gromit A Matter Of Loaf And Death', u'Wallace and Gromit A Close Shave', u'Wallace and Gromit A Grand Day Out', u'Wallace and Gromit The Curse of the Were-Rabbit', u'Watchmen', u'White Christmas', u'Who Framed Roger Rabbit', u'Wild Wild West', u'Wreck It Ralph', u'XMen First Class', u'XMen Origins Wolverine', u'Y tu mama tambien', u'Young Frankenstein', u'Your Highness', u'iblard time', u'sharktopus', u'shrek forever after']


class GetMovieMetadata(BaseTask):

    SECONDS = 1
    MAX_MOVIES = 10

    def __str__(self):
        return u"AddMovies"

    def do(self):
        qs = Movie.objects.filter(has_metadata=False).exclude(name__in=BAD_FILENAMES)
        total = qs.count()
        qs = qs[:self.MAX_MOVIES]
        if qs.count() == 0:
            gevent.sleep(100)
            return

        print "adding metadata for {} of {} movies".format(qs.count(), total)

        for movie in qs:
            try:
                movie.get_metadata()
                gevent.sleep(0)
            except Exception as e:
                print e
                raise
                # BAD_FILENAMES.append(movie.name)
                # print BAD_FILENAMES


class GetMovieRecommendations(BaseTask):

    SECONDS = 1
    MAX_MOVIES = 1

    def __str__(self):
        return u"AddMovies"

    def do(self):
        qs = Movie.objects.filter(has_metadata=True, has_recommendations=False)
        total = qs.count()
        qs = qs[:self.MAX_MOVIES]
        print "adding recommendations for {} of {} movies".format(qs.count(), total)

        if qs.count() == 0:
            gevent.sleep(100)
            return

        for movie in qs:
            recommendations = movie.get_recommendations()
            for m in recommendations:
                m.get_poster()
                gevent.sleep(0)
