from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


"""Module permettant de faire des opérations sur Twitter"""
class Bot_Twitter:

    def __init__(self, mail, password): #Création du Bot
        self.mail=mail
        self.password=password
        self.driver=webdriver.Chrome()


    #Connexion du bot à Twitter
    def connexion(self,website): #Connexion du Bot
        self.driver.get(website) #Connexion au site

        # On récupère l'emplacement du login
        emailInput=WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name*='email']")))
        passwordInput=WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name*='password']")))

        emailInput.send_keys(self.mail) #On envoie le mail
        passwordInput.send_keys(self.password) #On envoie le mdp
        passwordInput.send_keys(Keys.ENTER) #On clique sur entrer


    #Permet de se rendre sur le compte twitter de quelqu'un
    def go_to_account(self, account):
        self.driver.get("https://twitter.com/"+account)


    #Trouve tous les boutons d'une page
    def find_button(self):
        button=self.driver.find_elements_by_css_selector("div[role='button']")
        button=button+self.driver.find_elements_by_css_selector("a[role='button']")
        time.sleep(1)

        print("Nombre de boutton {}".format(len(button)))
        os.chdir('log')
        for i in range(len(button)):

            """On sauvegarde tout dans un fichier"""
            if i==0: #On regarde s'il existe déjà un fichier pour sauvegarder le log
                try:
                    os.remove("log boutton.txt")
                    print("suppression du fichier 'log button' existant")
                    fichier_boutton = open("log boutton.txt", "a")
                    fichier_boutton.write("Bouton {}".format(i + 1) + "\n")
                    fichier_boutton.write("Texte du boutton: {}".format(button[i].text) + "\n")
                    fichier_boutton.write("Classe du boutton: {}".format(button[i].get_attribute("class")) + "\n")
                    fichier_boutton.write(
                        "Balise html du boutton: {}".format(button[i].get_attribute("tagName")) + "\n")
                    fichier_boutton.write("\n")
                except:
                    fichier_boutton=open("log boutton.txt", "a")
                    fichier_boutton.write("Bouton {}".format(i+1)+"\n")
                    fichier_boutton.write("Texte du boutton: {}".format(button[i].text)+"\n")
                    fichier_boutton.write("Classe du boutton: {}".format(button[i].get_attribute("class"))+"\n")
                    fichier_boutton.write("Balise html du boutton: {}".format(button[i].get_attribute("tagName"))+"\n")
                    fichier_boutton.write("\n")
            else:
                fichier_boutton = open("log boutton.txt", "a")
                fichier_boutton.write("Bouton {}".format(i + 1) + "\n")
                fichier_boutton.write("Texte du boutton: {}".format(button[i].text) + "\n")
                fichier_boutton.write("Classe du boutton: {}".format(button[i].get_attribute("class")) + "\n")
                fichier_boutton.write("Balise html du boutton: {}".format(button[i].get_attribute("tagName")) + "\n")
                fichier_boutton.write("\n")

        if len(button)>0:
            print("Fin de l'écriture du fichier 'log button'")
            fichier_boutton.close()


    #Follow la personne dont on est sur la page
    def follow(self, account):
        self.go_to_account(account)

        try:
            follow = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div[data-testid$='-follow']")))
            follow.click()
            print("follow")
        except NoSuchElementException:
            print("Déjà suivi")



    #Unfollow la personne dont est sur la page
    def unfollow(self,account):
        self.go_to_account(account)

        try:
            #On clique une première fois sur unfollow
            unfollow = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div[data-testid$='-unfollow']")))
            unfollow.click()

            #On confirme
            unfollow = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div[data-testid='confirmationSheetConfirm']")))
            unfollow.click()
            print("unfollow")
        except:
            print("On ne suit pas cette personne")


    #On cherche tous les tweets qu'on peut retweeter
    def find_retweet(self):
        time.sleep(3)
        rt = self.driver.find_elements_by_css_selector("div[data-testid='retweet']")
        time.sleep(1)

        print("Nombre de tweets {}".format(len(rt)))
        os.chdir('log')
        for i in range(len(rt)):

            """On sauvegarde tout dans un fichier"""
            if i == 0:  # On regarde s'il existe déjà un fichier pour sauvegarder le log
                try:
                    os.remove("log retweet.txt")
                    print("suppression du fichier 'log retweet' existant")
                    fichier_retweet = open("log retweet.txt", "a")
                    fichier_retweet.write("Retweet {}".format(i + 1) + "\n")
                    fichier_retweet.write("Texte du Retweet: {}".format(rt[i].text) + "\n")
                    fichier_retweet.write("Classe du Retweet: {}".format(rt[i].get_attribute("class")) + "\n")
                    fichier_retweet.write("\n")
                except:
                    fichier_retweet = open("log retweet.txt", "a")
                    fichier_retweet.write("Retweet {}".format(i + 1) + "\n")
                    fichier_retweet.write("Texte du Retweet: {}".format(rt[i].text) + "\n")
                    fichier_retweet.write("Classe du Retweet: {}".format(rt[i].get_attribute("class")) + "\n")
                    fichier_retweet.write("\n")
            else:
                fichier_retweet = open("log retweet.txt", "a")
                fichier_retweet.write("Retweet {}".format(i + 1) + "\n")
                fichier_retweet.write("Texte du Retweet: {}".format(rt[i].text) + "\n")
                fichier_retweet.write("Classe du Retweet: {}".format(rt[i].get_attribute("class")) + "\n")
                fichier_retweet.write("\n")

        if len(rt) > 0:
            print("Fin de l'écriture du fichier 'log retweet'")
            fichier_retweet.close()


    #Le bot retweet des tweets
    def retweet(self, nb_retweets):

        """Première partie:
        On lance le bot qui doit trouver au moins 5 tweets à rt sur la page avant de continuer
        On stock ces boutons 'rt' dans une liste rt.
        On enregistre la longueur de cette liste pour savoir quand on l'aura parcourue entièrement"""

        self.driver.execute_script("window.scrollTo(0, 320)") #On fait glisser la page vers le bas pour charger les tweets
        rt=self.driver.find_elements_by_xpath("//div[@data-testid='retweet']")

        while len(rt)<2: #On veut au moins 2 rt pour commencer
            tweet = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//article[@role='article']")))
            tweet.send_keys(Keys.PAGE_DOWN)  # Si ça ne charge pas, on n'est pas descendu assez bas
            rt = self.driver.find_elements_by_xpath("//div[@data-testid='retweet']")
        longueur_liste_rt=len(rt)


        print("Nombre de rt: {}".format(longueur_liste_rt))


        """Deuxième partie: le clique
        On parcours chacun des éléments de la liste et on clique dessus une première fois puis une 2e 
        pour confirmer.
        A chaque fois qu'on clique, on regarde si on n'a pas une erreur
        Si on ne peut pas cliquer, on recommence (on reste dans la boucle while) car ça signifique qu'on a voulu cliquer 
        trop vite alors que la page n'avait pas encore fini de clqiuer sur le rt d'avant.
        Au bout de deux tentatives, on fait glisser la page vers le bas car ça signifie que si on ne peut pas cliquer
        c'est car il n'y a pas de boutons 'rt' sur notre écran."""

        a=1 #a va compter tous les tweets qu'on retweet
        numero_rt=0 #indice du tweet qu'on rt dans la liste 'rt'
        #Le bot rt chacun de ces retweets
        while a<=nb_retweets: #Tant qu'on a pas rt le nombre de tweets passés en paramètres

            print("clique sur le rt {}".format(a))
            premier_clique=False
            attente=0
            while premier_clique==False:
                try:
                    rt[numero_rt].click()
                except ElementClickInterceptedException:
                    attente+=1
                    if attente%2==0:
                        rt[numero_rt].send_keys(Keys.PAGE_DOWN)
                except StaleElementReferenceException:
                    pass
                else:
                    attente=0
                    premier_clique = True


            #Confirmation
            print("confirmation sur le rt {}".format(a))

            deuxieme_clique=False
            while deuxieme_clique==False:
                try:
                    self.driver.find_element_by_xpath("//div[@data-testid='retweetConfirm']").click()
                except ElementClickInterceptedException:
                    print("Trop rapide 2e clik")
                    pass
                except ElementNotInteractableException:
                    print("Pas encore chargé")
                    pass
                except NoSuchElementException:
                    print("Par encore chargé bis")
                    pass
                else:
                    deuxieme_clique=True
                    a += 1
                    numero_rt+=1


            """Troisième partie: On charge une nouvelle liste de rt
            Si on a retweet tous les tweets de la liste 'rt' initiale on en créé une autre pour rt les tweets suivants"""
            #On actualise la nouvelle liste de rt
            if a>longueur_liste_rt: #Si a parcouru tous les éléments de la liste rt on en créé une autre
                rt = self.driver.find_elements_by_xpath("//div[@data-testid='retweet']")
                numero_rt=0
                longueur_liste_rt+=len(rt)
                print("Liste de nouveaux retweets {}".format(len(rt)))


    #Le bot like des tweets
    def like(self, nb_like):

        self.driver.execute_script(
            "window.scrollTo(0, 320)")  # On fait glisser la page vers le bas pour charger les tweets
        like = self.driver.find_elements_by_xpath("//div[@data-testid='like']")

        while len(like) < 2:  # On veut au moins 2 like pour commencer
            tweet = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//article[@role='article']")))
            tweet.send_keys(Keys.PAGE_DOWN) #Si ça ne charge pas, on n'est pas descendu assez bas
            like = self.driver.find_elements_by_xpath("//div[@data-testid='like']")
        longueur_liste_like = len(like)

        print("Nombre de fav: {}".format(longueur_liste_like))

        a = 1  # a va compter tous les tweets qu'on like
        numero_like = 0  # indice du tweet qu'on rt dans la liste 'like'
        # Le bot like chacun de ces retweets
        while a <= nb_like:  # Tant qu'on a pas fav le nombre de tweets passés en paramètres

            print("clique sur le fav {}".format(a))
            premier_clique = False
            attente = 0
            while premier_clique == False:
                try:
                    like[numero_like].click()
                except ElementClickInterceptedException:
                    attente += 1
                    if attente % 2 == 0:
                        like[numero_like].send_keys(Keys.PAGE_DOWN)
                except StaleElementReferenceException:
                    pass
                else:
                    attente = 0
                    premier_clique = True
                    a+=1
                    numero_like+=1

            if a>longueur_liste_like: #Si a parcouru tous les éléments de la liste like on en créé une autre
                like = self.driver.find_elements_by_xpath("//div[@data-testid='like']")
                numero_like=0
                longueur_liste_like+=len(like)
                print("Liste de nouveaux likes {}".format(len(like)))


    #Fonction qui retweet et/ou like tous les nouveaux tweets de l'auteur
    def automatically(self, account, retweeter=True, liker=True):

        """Notre programme est une boucle infinie qui va rafrachir la page du compte dont on souhaite
        aimer/retweet les tweets. La boucle ne peut s'arrêter que manuellement, lorsqu'on ne souhaite plus faire
        ces opérations. En attendant, le compte de l'utilisateur est rafraîchi toutes les 8 secondes environ
        pour voir s'il y a de nouveaux tweets"""
        #k ici est un indicateur. Lorsque k=2 on ne cherche pas de nouveau tweets à aimer/ liker mais
        #on rafraichi la page. En effet, lorsque k=2 on aura chargé la page de l'utilisateur 2 fois
        #Or Twitter au bout de ces deux fois nous déconnecte automatiquement
        #Pour éviter un bug, on rafraichi la page uniquement si k=2
        k=1
        while 1:

            """Première partie: 
            On se rend sur le compte d'une personne
            On charge les listes de tweets où on peut mettre un like ou retweet"""

            time.sleep(5)
            self.go_to_account(account)
            self.driver.execute_script(
                "window.scrollTo(0, 100)")  # On fait glisser la page vers le bas pour charger les tweets
            time.sleep(2)

            rt = self.driver.find_elements_by_xpath("//div[@data-testid='retweet']")
            like=self.driver.find_elements_by_xpath("//div[@data-testid='like']")
            print("Longueur rt: {}".format(len(rt)))
            print("Longueur like: {}".format(len(like)))

            """Deuxième partie:
            Si k=2 on rafraichi la page
            Sinon on rt et/ou like tous les nouveaux tweets en fonction de ce qu'on veut
            """

            if k==2:
                #Quand on rafraichi la page la première fois on se déconnecte bizarrement
                #Du coup plutôt que d'avoir un bug on rafraichi la 2e fois qu'on se rend dans la boucle
                self.go_to_account(account)

            else:
                if min(len(rt),len(like))>0: #On utilise min pour éviter des "out of range"
                    for i in range(min(len(rt),len(like))):
                        #Si l'utilisateur veut retweet les nouveaux tweets
                        if retweeter==True:
                            premier_clique=False
                            attente=0
                            while not premier_clique:
                                try:
                                    rt[i].click()
                                except ElementClickInterceptedException:
                                    attente+=1
                                    if attente%2==0:
                                        rt[i].send_keys(Keys.PAGE_DOWN)
                                except ElementNotInteractableException:
                                    pass
                                else:
                                    premier_clique=True

                            deuxieme_clique=False
                            while not deuxieme_clique:
                                try:
                                    self.driver.find_element_by_xpath("//div[@data-testid='retweetConfirm']").click()
                                except ElementClickInterceptedException:
                                    pass
                                except ElementNotInteractableException:
                                    pass
                                except NoSuchElementException:
                                    pass
                                else:
                                    deuxieme_clique=True

                        #Si l'utilisateur veut liker les nouveaux tweets
                        if liker == True:
                            premier_clique = False
                            while not premier_clique:
                                try:
                                    like[i].click()
                                except ElementClickInterceptedException:
                                    pass
                                except ElementNotInteractableException:
                                    pass
                                else:
                                    premier_clique = True
            k+=1

    #Créer un compte Twitter
    def create_account(self,prenom, nom,):
        self.driver.get("https://twitter.com/i/flow/signup")

        #Clique sur 'Utiliser un email'
        email = WebDriverWait(self.driver,10).until(
            EC.element_to_be_clickable(
                (By.XPATH,"//div[@class='css-18t94o4 css-901oao r-1n1174f r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-19h5ruw r-bcqeeo r-qvutc0']")))
        email.click()

        #Seul moyen de récupurer tous les inputs
        name=self.driver.find_elements(By.CSS_SELECTOR,"input")

        name[0].send_keys(prenom + " " + nom)
        name[1].send_keys(self.mail)

        #Clique sur 'suivant'
        time.sleep(2)
        button_suivant_1 = WebDriverWait(self.driver,10).until(
            EC.element_to_be_clickable(
                (By.XPATH,"//div[@class='css-18t94o4 css-1dbjc4n r-urgr8i r-42olwf r-sdzlij r-1phboty r-rs99b7 r-1w2pmg r-1vsu8ta r-aj3cln r-1fneopy r-o7ynqc r-6416eg r-lrvibr']")))
        button_suivant_1.click()

        button_suivant_2 = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='css-18t94o4 css-1dbjc4n r-1q3imqu r-42olwf r-sdzlij r-1phboty r-rs99b7 r-1w2pmg r-1vsu8ta r-aj3cln r-1fneopy r-o7ynqc r-6416eg r-lrvibr']")))
        button_suivant_2.click()

        button_inscription = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='css-18t94o4 css-1dbjc4n r-urgr8i r-42olwf r-sdzlij r-1phboty r-rs99b7 r-1w2pmg r-19h5ruw r-1jayybb r-17bavie r-15bsvpr r-o7ynqc r-6416eg r-lrvibr']")))
        button_inscription.click()

        #On ouvre une nouvelle page Web
        page_2=webdriver.Chrome()
        pseudo=self.mail.split("@")[0]
        page_2.get("http://www.mailhazard.com/fr/" + pseudo + "/")

        #On récupère le code de vérification
        time.sleep(3)
        test_code=False
        compteur_tentative=0
        while not test_code:
            try:
                code=page_2.find_elements_by_css_selector("td[valign='middle']")
                code=code[3].text[0:6]

            except IndexError:
                compteur_tentative+=1
                if compteur_tentative==2:
                    renvoyer_mail=self.driver.find_element_by_xpath(
                        "//span[@class='css-18t94o4 css-901oao css-16my406 r-1n1174f r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0']")
                    renvoyer_mail.click()

                    confirm=self.driver.find_element_by_xpath(
                        "//div[@class='css-1dbjc4n r-1loqt21 r-18u37iz r-1j3t67a r-9qu9m4 r-o7ynqc r-6416eg r-13qz1uu']")
                    confirm.click()
                else:
                    time.sleep(10)
                    page_2.get("http://www.mailhazard.com/fr/" + pseudo + "/")

            except NoSuchElementException:
                compteur_tentative += 1
                if compteur_tentative == 2:
                    renvoyer_mail = self.driver.find_element_by_xpath(
                        "//span[@class='css-18t94o4 css-901oao css-16my406 r-1n1174f r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0']")
                    renvoyer_mail.click()

                    confirm = self.driver.find_element_by_xpath(
                        "//div[@class='css-1dbjc4n r-1loqt21 r-18u37iz r-1j3t67a r-9qu9m4 r-o7ynqc r-6416eg r-13qz1uu']")
                    confirm.click()
                else:
                    time.sleep(10)
                    page_2.get("http://www.mailhazard.com/fr/" + pseudo + "/")
            else:
                test_code=True
        print(code)
        page_2.quit()

        #On entre le code
        code_test=False
        while not code_test:
            try:
                codeInput=self.driver.find_element(By.CSS_SELECTOR,"input")
            except NoSuchElementException:
                pass
            except ElementNotInteractableException:
                pass
            except ElementClickInterceptedException:
                pass
            else:
                code_test=True
        codeInput.send_keys(code)

        #On passe à la page d'après
        button_suivant_3 = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='css-18t94o4 css-1dbjc4n r-urgr8i r-42olwf r-sdzlij r-1phboty r-rs99b7 r-1w2pmg r-1vsu8ta r-aj3cln r-1fneopy r-o7ynqc r-6416eg r-lrvibr']")))
        button_suivant_3.click()

        #On entre le mot de passe
        mdp_test=False
        while not mdp_test:
            try:
                mdp=self.driver.find_element_by_xpath("//input[@class='r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-1inuy60 r-utggzx r-vmopo1 r-1w50u8q r-1lrr6ok r-1dz5y72 r-1ttztb7 r-13qz1uu']")
            except NoSuchElementException:
                pass
            except ElementNotInteractableException:
                pass
            except ElementClickInterceptedException:
                pass
            else:
                mdp_test=True
        mdp.send_keys(self.password)

        #On passe à la page d'après
        button_suivant_4 = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='css-1dbjc4n r-urgr8i r-42olwf r-sdzlij r-1phboty r-rs99b7 r-1w2pmg r-1vsu8ta r-aj3cln r-icoktb r-1fneopy r-o7ynqc r-6416eg r-lrvibr']")))
        button_suivant_4.click()

        #On ne met pas de photo et on passe à la page d'après
        button_passer_pour_le_moment = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='css-18t94o4 css-1dbjc4n r-1niwhzg r-42olwf r-sdzlij r-1phboty r-rs99b7 r-1w2pmg r-1vsu8ta r-aj3cln r-1fneopy r-o7ynqc r-6416eg r-lrvibr']")))
        button_passer_pour_le_moment.click()





bot=Bot_Twitter("pau1l877tee785@mailHazard.com","Simon1998")
bot.create_account("Simon", "testeur")




