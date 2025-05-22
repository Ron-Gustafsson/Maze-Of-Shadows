# TEE PELI TÄHÄN
import pygame
import sys
import random

class MazeofShadows:
    def __init__(self):
        pygame.init()
        
        self.ruudun_koko = 48 # tai 32, 48, 64 - määrittää ruudun pikselikoon
        self.lataa_kuvat() # Ladataan pelissä käytettävät kuvat
        pygame.display.set_caption("Maze of Shadows") # Ikkunaan otsikko

        # Kenttäasetukset
        self.alkuperaiset_elamat = 5
        self.kentat = [         # Kenttä merkkijonoina, jokainen rivi on yksi labyrintin rivi, 21 x 15 kenttä
            [
                "#####################",
                "#P....S#o...S#o....E#",
                "#.###.#####.#####.###",
                "#...#.#S....#S#.....#",
                "###.#.#.#.###o#.###.#",
                "#...#...#.....#.#.o.#",
                "#.###########.#.#.#.#",
                "#.#..M......#.#.#.#.#",
                "#.#.###.###.#.#.#.#.#",
                "#.#.#.....#.#.#.S.#.#",
                "#.#.#.###.#.#.#.#.#.#",
                "#.#.#.#..o#.#.#.#.#.#",
                "#.#.#.#S###.#.#.#.#M#",
                "#o..................#",
                "#####################"
            ],
            [
                "#####################",
                "#P..#o......#E......#",
                "#.#.#.##.##.#.###.#.#",
                "#.#.#.#...#.#...#.#.#",
                "#.#.#.#.#.#.###.#.#.#",
                "#...#.#.#.#o....#.#.#",
                "##.#S.#.#.#######.#o#",
                "#.....#.#.......#.S.#",
                "#.#####.#######.#.#M#",
                "#.#o..M.#.....#.#.#.#",
                "#.#o..###.###.#.#.#.#",
                "#.#####M#.#S#.#.#.#.#",
                "#.#S..#...#o#.#.#.#o#",
                "#o................M.#",
                "#####################"
            ],
            [
                "#####################",
                "#P....#o...o#......E#",
                "##.##.##S.S##.#oo#.##",
                "#..#o.#.....#.M....M#",
                "#.###.#.###.#.###.#.#",
                "#...#.#.#o#.#.#o#..o#",
                "###.#.#.#.#.#.#.#####",
                "#o..#...S.S...#.....#",
                "#.#####.#M#######.#.#",
                "#.#...#o#.......#.#.#",
                "#.#.#.###.#.##S.#.#.#",
                "#.#.#o....#.#o..#.#.#",
                "#.#.#####.#.#####.#.#",
                "#.M...o.......o...M.#",
                "#####################"
            ]
            # [
            #     "#####################",
            #     "#P..#o....#.....#..E#",
            #     "###.#.###.#.###.#.###",
            #     "#...#...#.#...#.#...#",
            #     "#.#####.#.###.#.###.#",
            #     "#.#.....#.#...#.....#",
            #     "#.#.#####.#.#######.#",
            #     "#.#.....#...#.....#.#",
            #     "#.#####.###.#.###.#.#",
            #     "#.....#.....#.#...#.#",
            #     "#####.#######.#.###.#",
            #     "#o..#.#.oo..#.#.....#",
            #     "#.#.#.#.#S#.#.#######",
            #     "#.................Mo#",
            #     "#####################"
            # ]
        ]
        # --- Merkkien selitykset ---
        # pelaaja = P
        # exit ovi = E
        # seinä = #
        # lattia = .
        # kolikko = o
        # liikkuva hirviö = M
        # paikallaan hirviö = S

        # Aseta alkutila valikkoon
        self.pelitila = "valikko"
        self.valikon_kohdat = ["New Game", "Exit Game", "Later ↓", "Continue Game", "Level Select", "Settings"]
        self.valittu_kohta = 0
        self.kentan_numero = 0
        self.kello = pygame.time.Clock()
        self.peli_kaynnissa = True

        # Valot päälle asetus
        self.nayta_valot = False # F-näppäin näyttää koko kentän
        self.suunta = (0, 0) # Viimeisin liikesuunta
        self.nahdyt_ruudut = set()

        self.elamat = self.alkuperaiset_elamat  # TÄRKEÄÄ!
        self.fontti = pygame.font.SysFont("Arial", 24, bold=True)

        # Luo perusnäyttö valikkoa varten
        self.naytto = pygame.display.set_mode((1024, 768))
        self.pelisilmukka()

    def lataa_kuvat(self):
        # Ladataan ja skaalataan kuvat ruudun kokoon
        self.kuvat = []
        for nimi in ["robo", "hirvio", "kolikko", "ovi"]:
            kuva = pygame.image.load(nimi + ".png")
            kuva = pygame.transform.scale(kuva, (self.ruudun_koko, self.ruudun_koko))
            self.kuvat.append(kuva)

    def uusi_peli(self):
        self.peliaika_alkoi = pygame.time.get_ticks()  # Nollaa aikalaskurin
        self.kentta = list(self.kentat[self.kentan_numero])  # tehdään kopio kentästä, ettei alkuperäinen muutu

        # Kentän korkeus ja leveys ruutuina
        self.kentan_korkeus = len(self.kentta)
        self.kentan_leveys = len(self.kentta[0])

        # Alapalkin korkeus (sama kuin yksi ruutu, jotta näyttää yhtenäiseltä)
        self.alapalkki_korkeus = self.ruudun_koko

        # Näytön korkeus ja leveys pikseleinä:
        # → kenttä + alapalkki piirretään päällekkäin
        nayton_leveys = self.ruudun_koko * self.kentan_leveys
        nayton_korkeus = self.ruudun_koko * self.kentan_korkeus + self.alapalkki_korkeus

        # Luodaan näyttö, johon mahtuu kenttä + alapalkki
        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus))

        # Etsii pelaajan aloituspaikan, tallentaa koordinaatit ja poistaa P-merkin kartasta (jotta pelaajaa ei piirretä enää kartan perusteella)
        for rivi, rivi_teksti in enumerate(self.kentta):
            for sarake, merkki in enumerate(rivi_teksti):
                if merkki == "P":
                    self.pelaaja_x = sarake
                    self.pelaaja_y = rivi
                    # Muutetaan kentässä pelaajan paikka lattiaksi
                    self.kentta[rivi] = rivi_teksti[:sarake] + "." + rivi_teksti[sarake+1:]
                    break
        
        # Alustetaan kolikot
        self.kolikot = 0
        # Lasketaan kolikoiden määrä kartasta
        self.kolikoita_yhteensa = sum(rivi.count("o") for rivi in self.kentta)

        # Alustetaan hirviöt ja kehitetään liike niille
        self.hirviot = []

        # Käydään kentän merkit läpi
        for y, rivi in enumerate(self.kentta):
            for x, merkki in enumerate(rivi):

                # Pelaajan aloituspaikka
                if merkki == "P":
                    self.pelaaja_x = x
                    self.pelaaja_y = y
                    self.kentta[y] = rivi[:x] + "." + rivi[x+1:] # Korvataan pelaaja kartassa lattialla

                # Liikkuva hirviö
                elif merkki == "M":
                    self.hirviot.append({
                        "x": x, "y": y,
                        "dx": 1, "dy": 0, # aloittaa liikkeellä oikealle
                        "tyyppi": "liikkuva",
                        "liikelaskuri":  0 # asetetaan liikelaskuri rajoittamaan liikettä
                    })
                    self.kentta[y] = rivi[:x] + "." + rivi[x + 1:] # Korvataan hirviö kartassa lattialla

                    # Paikallaan pysyvä hirviö
                elif merkki == "S":
                    self.hirviot.append({
                        "x": x, "y": y,
                        "dx": 0, "dy": 0, # ei liiku
                        "tyyppi": "paikallaan"
                    })
                    self.kentta[y] = rivi[:x] + "." + rivi[x+1:] # Korvataan hirviö kartassa lattialla

        self.nahdyt_ruudut = set() # Nollataan nähdyt ruudut, jotta uusi peli alkaa varjon kanssa

    def piirra_kentta(self):
        for rivi, rivi_teksti in enumerate(self.kentta):
            for sarake, merkki in enumerate(rivi_teksti):
                x = sarake * self.ruudun_koko
                y = rivi * self.ruudun_koko

                random.seed(123)  # kiinteä satunnaissiementäjä
                if merkki == "#":  # SEINÄ
                    perusvari = (65, 40, 30)  # tumman ruskea kiviseinä (45, 30, 20)
                    vaihtelu = random.randint(-10, 10)
                else:  # LATTIAT ym.
                    perusvari = (75, 75, 85)  # tummahko lattia (65, 65, 65)
                    vaihtelu = random.randint(-10, 10)

                # Luo sävy satunnaisvaihtelulla
                vari = tuple(max(0, min(255, v + vaihtelu)) for v in perusvari)

                pygame.draw.rect(self.naytto, vari, (x, y, self.ruudun_koko, self.ruudun_koko))

                # Piirretään kuvat (pelaajaa ei piirretä vielä tässä) Poistin hirvion ettei tule kahteen kertaan.
                if merkki == "o":
                    self.naytto.blit(self.kuvat[2], (x, y))  # kolikko
                elif merkki == "E":
                    self.naytto.blit(self.kuvat[3], (x, y))  # ovi

    def piirra_pelaaja(self):
        x = self.pelaaja_x * self.ruudun_koko
        y = self.pelaaja_y * self.ruudun_koko

        self.naytto.blit(self.kuvat[0], (x, y)) # piirtää robo.png

    def piirra_hirviot(self):
        for hirvio in self.hirviot:
            # lasketaan piirto-koordinaatit pikseleina
            x = hirvio["x"] * self.ruudun_koko
            y = hirvio["y"] * self.ruudun_koko

            # Piirretään hirviön kuva
            self.naytto.blit(self.kuvat[1], (x, y))

    def piirra_naytto(self):
        self.piirra_kentta()
        self.piirra_hirviot()
        self.piirra_pelaaja()
        self.piirra_alapalkki()

        # --- Pelaajan näkyvyyden hallinta ---
        if not hasattr(self, "nahdyt_ruudut"):
            self.nahdyt_ruudut = set()

        # Luodaan 3x3 näkyvyys pelaajan ympärille. dx = delta x → muutos x-suunnassa (vasen–oikea), dy = delta y → muutos y-suunnassa (ylös–alas)
        for dx in range(-1, 2): # esim 3x3 -1, 2 5x5 -2, 3
            for dy in range(-1, 2):
                x = self.pelaaja_x + dx
                y = self.pelaaja_y + dy 
                if 0 <= x < self.kentan_leveys and 0 <= y < self.kentan_korkeus: # Lisää ympäröivät ruudut nähtyihin – riippumatta onko valot päällä
                    self.nahdyt_ruudut.add((x, y))

        if not self.nayta_valot:
            sade_ruuduissa = 1.5
            sade_px = int(sade_ruuduissa * self.ruudun_koko)

            # Laske kentän koko (ilman alapalkkia)
            kentta_leveys = self.kentan_leveys * self.ruudun_koko
            kentta_korkeus = self.kentan_korkeus * self.ruudun_koko

            # Luo varjopinta vain kentän alueelle
            varjo = pygame.Surface((kentta_leveys, kentta_korkeus), pygame.SRCALPHA)
            varjo.fill((0, 0, 0, 210))  # himmennetty taustavarjo, säädä tästä kirkkautta

            # Pelaajan keskipiste
            cx = int(self.pelaaja_x * self.ruudun_koko + self.ruudun_koko // 2)
            cy = int(self.pelaaja_y * self.ruudun_koko + self.ruudun_koko // 2)

            # Kellertävä valosävy (voit säätää RGB:tä)
            valo_vari = (200, 160, 20)

            # Piirrä valo sisemmästä ulkoreunaan
            for r in range(sade_px, 0, -1):
                kirkkaus = 70  # max läpinäkyvyys (säädä!)
                alpha = int(kirkkaus * (r / sade_px))
                pygame.draw.circle(varjo, (*valo_vari, alpha), (cx, cy), r)

            self.naytto.blit(varjo, (0, 0))

        pygame.display.flip()


    def kasittele_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:  # Suljetaan peli X:stä
                self.lopeta_peli()

            # Käsitellään näppäimistökomennot
            elif tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_ESCAPE:
                    if self.pelitila in ["kentan_lapaisy", "pelivoitettu"]:
                        self.pelitila = "valikko"
                    else:
                        self.lopeta_peli()
                elif tapahtuma.key == pygame.K_m:
                    if self.pelitila in ["kentan_lapaisy", "pelivoitettu"]:
                        self.pelitila = "valikko"

                # Kentän peiton toimivuus ja valot päälle F-nappi
                elif tapahtuma.key == pygame.K_f:
                    self.nayta_valot = True

                elif tapahtuma.key == pygame.K_s: # Kenttäsuunnitteluun s-näppäin level complete
                    self.ohita_kentta()

                # Valikkonäppäimet
                if self.pelitila == "valikko":
                    if tapahtuma.key == pygame.K_UP:
                        self.valittu_kohta = (self.valittu_kohta - 1) % len(self.valikon_kohdat)
                    elif tapahtuma.key == pygame.K_DOWN:
                        self.valittu_kohta = (self.valittu_kohta + 1) % len(self.valikon_kohdat)
                    elif tapahtuma.key == pygame.K_RETURN:
                        valinta = self.valikon_kohdat[self.valittu_kohta]
                        if valinta == "New Game":
                            self.aloita_koko_peli_alusta()
                        elif valinta == "Exit Game":
                            self.lopeta_peli()
                        # voit lisätä tänne muitakin kohtia myöhemmin

                # F1-näppäin
                elif tapahtuma.key == pygame.K_F1:
                    if self.pelitila == "valikko":
                        self.aloita_koko_peli_alusta()
                    elif self.pelitila == "kentan_lapaisy":
                        self.uusi_peli()
                        self.pelitila = "peli"
                    elif self.pelitila in ["gameover", "pelivoitettu"]:
                        self.aloita_koko_peli_alusta()
                    else:
                        self.aloita_sama_kentta_alusta(vahenna_elama=False) # Ei vähennä enää valinta ikkunoissa elämiä

                # ENTER kentän läpäisyn jälkeen
                elif tapahtuma.key == pygame.K_RETURN:
                    if self.pelitila == "kentan_lapaisy":
                        self.siirry_seuraavaan_kenttaan()

                # Nuolinäppäimet toimivat vain varsinaisessa pelitilassa
                elif self.pelitila == "peli":
                    if tapahtuma.key == pygame.K_UP:
                        self.liikuta_pelaajaa(0, -1)
                    elif tapahtuma.key == pygame.K_DOWN:
                        self.liikuta_pelaajaa(0, 1)
                    elif tapahtuma.key == pygame.K_LEFT:
                        self.liikuta_pelaajaa(-1, 0)
                    elif tapahtuma.key == pygame.K_RIGHT:
                        self.liikuta_pelaajaa(1, 0)

            # F-napin vapautus loppuun ettei muut sekoile ja peli kaadu
            elif tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_f:
                    self.nayta_valot = False

    def pelisilmukka(self):
        while self.peli_kaynnissa:
            self.kasittele_tapahtumat()

            # Piirrä eri näyttö pelitilan mukaan
            if self.pelitila == "valikko": # Piirretään valikko
                self.piirra_valikko()
            elif self.pelitila == "peli": # normaali pelitilanne
                self.paivita_hirviot()
                self.kasittele_hirvio_tormays()
                self.piirra_naytto()         
            elif self.pelitila == "gameover": # kun elämät loppuvat
                self.piirra_gameover()       
            elif self.pelitila == "kentan_lapaisy": # Kenttä läpäisty
                self.piirra_kentan_lapaisy()
            elif self.pelitila == "pelivoitettu": # Peli läpi
                self.piirra_peli_lapaisty()   

            # Rajoitetaan nopeutta
            self.kello.tick(60)
        self.lopeta_peli

    def liikuta_pelaajaa(self, siirto_x, siirto_y):
        self.suunta = (siirto_x, siirto_y)  # MUISTIIN! Liittyy kentän peittämiseen
        uusi_x = self.pelaaja_x + siirto_x
        uusi_y = self.pelaaja_y + siirto_y
        kohde = self.kentta[uusi_y][uusi_x]

        # Estetään seinään meno
        if kohde == "#":
            return

        # Kolikon keruu
        if kohde == "o":
            self.kolikot += 1
            # Poistetaan kolikko kartasta
            rivi = self.kentta[uusi_y]
            self.kentta[uusi_y] = rivi[:uusi_x] + "." + rivi[uusi_x + 1:]
        
        # Oven saavuttaminen
        if kohde == "E":
            if self.kolikot == self.kolikoita_yhteensa: # Jos kolikot kerätty kentta lapaisty
                self.pelitila = "kentan_lapaisy"
                return

        # Päivitetään pelaajan paikka
        self.pelaaja_x = uusi_x
        self.pelaaja_y = uusi_y

    def paivita_hirviot(self):
        for hirvio in self.hirviot:
            if hirvio["tyyppi"] != "liikkuva":
                continue

            # Lisätään laskuri rajoittamaan hirvioiden nopeutta
            hirvio["liikelaskuri"] += 1
            if hirvio["liikelaskuri"] < 50: # arvo kuinka monta framea
                continue
            hirvio["liikelaskuri"] = 0 # nollaa laskurin

            # Lasketaan uusi paikka
            uusi_x = hirvio["x"] + hirvio["dx"]
            uusi_y = hirvio["y"] + hirvio["dy"]

            # Jos uusi paikka ei ole seinä, siirrytään sinne
            if self.kentta[uusi_y][uusi_x] != "#":
                hirvio["x"] = uusi_x
                hirvio["y"] = uusi_y
            else:
                # Käännetään suunta: yritetään liikkua ylös/alas jos sivusuunta ei onnistu
                alku_dx = hirvio["dx"]
                alku_dy = hirvio["dy"]

                # Vaihdetaan suuntaa: oikea → vasen, tai alas → ylös
                hirvio["dx"] *= -1
                hirvio["dy"] *= -1

                uusi_x = hirvio["x"] + hirvio["dx"]
                uusi_y = hirvio["y"] + hirvio["dy"]

                # Jos käännetty suunta toimii, liikutaan sinne
                if self.kentta[uusi_y][uusi_x] != "#":
                    hirvio["x"] = uusi_x
                    hirvio["y"] = uusi_y
                else:
                    # Jos ei voi liikkua kumpaankaan suuntaan, kokeillaan vaihtaa suuntaa y-akselille
                    mahdolliset_suunnat = [(0, 1), (0, -1)]  # alas tai ylös

                    for dx, dy in mahdolliset_suunnat:
                        tarkista_x = hirvio["x"] + dx
                        tarkista_y = hirvio["y"] + dy
                        if self.kentta[tarkista_y][tarkista_x] != "#":
                            hirvio["dx"] = dx
                            hirvio["dy"] = dy
                            hirvio["x"] = tarkista_x
                            hirvio["y"] = tarkista_y
                            break

    def kasittele_hirvio_tormays(self):
        for hirvio in self.hirviot:
            if hirvio["x"] == self.pelaaja_x and hirvio["y"] == self.pelaaja_y: # Jos hirviö on samassa ruudussa pelaajan kanssa
                self.nayta_kuolema_ravistus()
                self.aloita_sama_kentta_alusta()
                return

    def piirra_alapalkki(self):
        # Alapalkin yläreunan y-koordinaatti (kentän jälkeen)
        y = self.kentan_korkeus * self.ruudun_koko

        # Alapalkin taustaväri ja koko
        taustavari = (20, 20, 20)  # tumma harmaa tausta
        pygame.draw.rect(self.naytto, taustavari, (0, y, self.naytto.get_width(), self.alapalkki_korkeus))

        # Fontit
        sydan_fontti = pygame.font.SysFont("Arial", 32, bold=True)
        ohje_fontti = pygame.font.SysFont("Arial", 24)

        # Tekstivärit
        vari_kolikot = (255, 215, 0)  # kulta
        vari_aika = (255, 255, 255)   # valkoinen
        vari_sydan = (255, 60, 60)  # kirkas punainen sydämen väri
        vari_ohje = (200, 200, 200) # vihreä

        # --- Kentän numero ---
        teksti_kentta = self.fontti.render(f"Level: {self.kentan_numero + 1}", True, (100, 200, 255))  # sinertävä väri
        self.naytto.blit(teksti_kentta, (20, y + 5))

        # ----- Kolikkojen määrä -----
        teksti_kolikot = self.fontti.render(f"Coins: {self.kolikot} / {self.kolikoita_yhteensa}", True, vari_kolikot)
        self.naytto.blit(teksti_kolikot, (110, y + 5))

        # ----- Kulunut aika sekunteina -----
        kulunut = int((pygame.time.get_ticks() - self.peliaika_alkoi) / 1000) # Jotta toimisi myös game over jälkeen, alkaa nollasta
        minuutit = kulunut // 60
        sekunnit = kulunut % 60
        teksti_aika = self.fontti.render(f"Time: {minuutit:02}:{sekunnit:02}", True, vari_aika)
        self.naytto.blit(teksti_aika, (240, y + 5))  # ↤ vaihda 300 jos haluat eri kohtaan

        # ----- Elämät tekstinä sydäminä -----
        sydan_fontti = pygame.font.SysFont("Arial", 32, bold=True)
        sydamet = " ".join(["\u2665" for _ in range(self.elamat)])
        teksti_sydamet = sydan_fontti.render(sydamet, True, vari_sydan)
        self.naytto.blit(teksti_sydamet, (360, y + 2))

        # --- Ohjetekstit ---
        teksti_ohje = ohje_fontti.render("MOVE: ← ↑ → ↓   RESTART: F1   QUIT: ESC", True, vari_ohje)
        x = self.naytto.get_width() - teksti_ohje.get_width() - 10
        self.naytto.blit(teksti_ohje, (x, y + 6))

    # --- Kuolema efekti peliin ---
    def nayta_kuolema_ravistus(self):
        for _ in range(20):  # monta kertaa piirretään ravistettuna
            dx = random.randint(-5, 5)
            dy = random.randint(-5, 5)

            self.naytto.fill((0, 0, 0))  # tyhjennä tausta

            # Piirretään kenttä ja pelaaja siirtyneenä
            self.piirra_kentta_siirretty(dx, dy)
            self.piirra_pelaaja_siirretty(dx, dy)

            pygame.display.flip()
            pygame.time.delay(30)

    def piirra_kentta_siirretty(self, siirto_x, siirto_y):
        for rivi, rivi_teksti in enumerate(self.kentta):
            for sarake, merkki in enumerate(rivi_teksti):
                x = sarake * self.ruudun_koko + siirto_x
                y = rivi * self.ruudun_koko + siirto_y

                if merkki == "#":
                    pygame.draw.rect(self.naytto, (70, 40, 20), (x, y, self.ruudun_koko, self.ruudun_koko))
                else:
                    pygame.draw.rect(self.naytto, (255, 0, 0), (x, y, self.ruudun_koko, self.ruudun_koko))

                if merkki == "M":
                    self.naytto.blit(self.kuvat[1], (x, y))
                elif merkki == "o":
                    self.naytto.blit(self.kuvat[2], (x, y))
                elif merkki == "E":
                    self.naytto.blit(self.kuvat[3], (x, y))

    def piirra_pelaaja_siirretty(self, siirto_x, siirto_y):
        x = self.pelaaja_x * self.ruudun_koko + siirto_x
        y = self.pelaaja_y * self.ruudun_koko + siirto_y
        self.naytto.blit(self.kuvat[0], (x, y))
    # --- Kuolema efekti päättyy ---

    def aloita_sama_kentta_alusta(self, vahenna_elama=True): # Tällä estetään elämien vähennys F1 ikkunoissa
        self.uusi_peli()  
        if vahenna_elama: # Jos pelaaja kuolee vähennetään elämä
            self.elamat -= 1
            if self.elamat <= 0: # Jos elämät 0 koittaa gameover
                self.pelitila = "gameover"

    def aloita_koko_peli_alusta(self):
        self.kentan_numero = 0  # alkaa nollasta ja kasvatetaan siirry seuraavaan kenttaan
        self.peliaika_alkoi = pygame.time.get_ticks()  # Kello alkaa alusta game over jälkeen
        self.elamat = self.alkuperaiset_elamat
        self.pelitila = "peli"
        self.uusi_peli()

    def siirry_seuraavaan_kenttaan(self):
        self.kentan_numero += 1
        if self.kentan_numero >= len(self.kentat):
            self.pelitila = "pelivoitettu"
        else:
            self.pelitila = "peli"
            self.uusi_peli()

    def piirra_tekstit_keskelle(self, otsikkorivit, ohjeet, otsikon_vari=(0, 255, 0), korosta_indeksi=None):
        self.naytto.fill((0, 0, 0))  # Tyhjennä ruutu

        otsikko_fontti = pygame.font.SysFont("Arial", 60, bold=True)
        ohje_fontti = pygame.font.SysFont("Arial", 24)

        # Määritä alku y-koordinaatti (muokkaa tarvittaessa)
        alku_y = self.naytto.get_height() // 2 - (len(otsikkorivit) * 40 + 40)

        # Piirrä kaikki otsikkorivit
        for i, rivi in enumerate(otsikkorivit):
            otsikko_teksti = otsikko_fontti.render(rivi, True, otsikon_vari)
            otsikko_x = self.naytto.get_width() // 2 - otsikko_teksti.get_width() // 2
            otsikko_y = alku_y + i * 70
            self.naytto.blit(otsikko_teksti, (otsikko_x, otsikko_y))

        # Piirrä ohje-/valikkorivit otsikon jälkeen
        for i, rivi in enumerate(ohjeet):
            vari = (255, 255, 0) if i == korosta_indeksi else (200, 200, 200)
            ohje_teksti = ohje_fontti.render(rivi, True, vari)
            ohje_x = self.naytto.get_width() // 2 - ohje_teksti.get_width() // 2
            ohje_y = alku_y + len(otsikkorivit) * 70 + 20 + i * 30
            self.naytto.blit(ohje_teksti, (ohje_x, ohje_y))
        pygame.display.flip()

    def piirra_valikko(self):
        self.naytto.fill((0, 0, 0))

        otsikko_fontti = pygame.font.SysFont("Arial", 60, bold=True)
        kohta_fontti = pygame.font.SysFont("Arial", 36)

        otsikko = otsikko_fontti.render("MAZE OF SHADOWS", True, (0, 180, 255))
        otsikko_x = self.naytto.get_width() // 2 - otsikko.get_width() // 2
        self.naytto.blit(otsikko, (otsikko_x, 100))

        for i, teksti in enumerate(self.valikon_kohdat):
            vari = (255, 255, 0) if i == self.valittu_kohta else (200, 200, 200)
            kohta = kohta_fontti.render(teksti, True, vari)
            x = self.naytto.get_width() // 2 - kohta.get_width() // 2
            y = 220 + i * 50
            self.naytto.blit(kohta, (x, y))

        # --- Tekijälle kunnianosoitus eli minulle ---
        teksti1 = self.fontti.render("Created by Ron Gustafsson", True, (180, 180, 180))
        teksti2 = self.fontti.render("Python Programming MOOC: Advanced Course in Programming", True, (180, 180, 180))

        # Skaalataan tekstit jos näytön koko muuttuu (ei kiinteitä pikseleitä vaan suhteutetaan prosenteilla)
        x1 = self.naytto.get_width() // 2 - teksti1.get_width() // 2
        x2 = self.naytto.get_width() // 2 - teksti2.get_width()// 2
        y2 = self.naytto.get_height() * 0.92 # esim 92% alareunasta
        y1 = y2 - 35 # Pieni väli ylätekstiin
        
        self.naytto.blit(teksti1, (x1, y1))
        self.naytto.blit(teksti2, (x2, y2))

        pygame.display.flip()

    def piirra_kentan_lapaisy(self):
        self.piirra_tekstit_keskelle(
            ["LEVEL COMPLETE!"],
            ["Next Level → Press ENTER", "Restart Level → Press F1", "Main Menu → Press M"],
            otsikon_vari=(0, 255, 0)  # vihreä
        )

    def piirra_peli_lapaisty(self):
        self.piirra_tekstit_keskelle(
            [
                "You discovered the path", 
                "to the end",
                "of the Maze of Shadows!",
                "Congratulations!"
            ],
            ["Restart Game → Press F1", "Main Menu → Press M", "Quit Game → Press ESC"],
            otsikon_vari=(255, 215, 0)
        )

    def piirra_gameover(self):
        self.piirra_tekstit_keskelle(
            ["GAME OVER!"],
            ["Restart Game → Press F1", "Quit Game → Press ESC"],
            otsikon_vari=(255, 0, 0)  # punainen
        )

    def lopeta_peli(self):
        self.peli_kaynnissa = False #Lopettaa pelin turvallisesti eri ympäristöissä .py .exe
        pygame.quit()
        sys.exit()

    # --- Kenttäsuunnitteluun level complete s-napista
    def ohita_kentta(self):
        # Merkitään kaikki kolikot kerätyiksi
        self.kolikot = self.kolikoita_yhteensa

        # Etsitään oven sijainti kentästä
        for y, rivi in enumerate(self.kentta):
            for x, merkki in enumerate(rivi):
                if merkki == "E":
                    self.pelaaja_x = x
                    self.pelaaja_y = y
                    self.pelitila = "kentan_lapaisy"
                    return

if __name__ == "__main__":
    MazeofShadows()