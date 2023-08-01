from app import app
from models import db, User, Charity, Donation, Beneficiary, Inventory
from faker import Faker
import markovify
import random
from werkzeug.security import generate_password_hash

print("Seeding has started.")

fake = Faker()

with app.app_context():
    db.drop_all()
    db.create_all()

    def generte_random_text(text_corpus, max_length=255):
        text_model = markovify.Text(text_corpus)
        return text_model.make_sentence(max_length=max_length)
    
    #The below block of code will now be used to train the markov to generate good random text
    caption_corpus = """
        The school received a donation of new textbooks and supplies.
        Thanks to your generosity, families now have access to clean water.
        With your help, we provided warm blankets to those in need during the winter.
        Children in the village were overjoyed when they received new toys.
        Our efforts ensured that pregnant women have access to proper prenatal care.
        The community celebrated as we inaugurated the new medical clinic.
        Donors like you have made it possible to build new classrooms for the students.
        Families were grateful for the distribution of food packages during the crisis.
        Thanks to your contributions, we installed solar panels for sustainable energy.
        The community now has a thriving vegetable garden to combat hunger.
        Your donations allowed us to train local teachers for better education.
        Children's smiles brightened up the school as they received new uniforms.
        The medical mission treated hundreds of patients in remote areas.
        Vocational training programs have empowered women to start businesses.
        Your support helped us build safe homes for those affected by disasters.
        We distributed hygiene kits to prevent the spread of diseases.
        The community center is now equipped with computers for educational purposes.
        With your assistance, we repaired damaged roads for better transportation.
        Funds were used to construct a playground for the children to play safely.
        New sewing machines have provided job opportunities for women.
        We established a library to encourage a culture of reading.
        Your contributions provided essential medical equipment for the clinic.
        The educational scholarship program has changed many young lives.
        We organized workshops to raise awareness about health and hygiene.
        Thanks to your donations, we installed a water purification system.
        The charity event raised funds to sponsor education for underprivileged kids.
        You made it possible for us to distribute warm clothing during the winter.
        We conducted vocational training to empower youth for a brighter future.
        The community garden project improved access to nutritious food.
        Your generosity enabled us to support elderly citizens with basic necessities.
        The medical team provided free eye exams and glasses to those in need.
        We implemented a waste management program for a cleaner environment.
        Families received emergency relief kits during natural disasters.
        Children in remote areas now have access to quality education.
        Your support allowed us to establish a mobile health clinic.
        We distributed mosquito nets to prevent malaria in vulnerable communities.
        The charity walk raised awareness and funds for the cause.
        Villagers celebrated the inauguration of the new community center.
        Thanks to you, we installed a clean water well in the village.
        We conducted workshops on financial literacy to empower women.
        Your contributions helped us build a playground for disabled children.
        The medical mission treated patients with free medical check-ups.
        The vocational training center offers new opportunities for the youth.
        We distributed seeds and farming tools to improve agricultural practices.
        Your donations supported the vaccination drive for children.
        We renovated a school building to create a better learning environment.
        The community now has access to a reliable source of electricity.
        Thanks to your contributions, we rescued and rehabilitated injured animals.
        Families received essential groceries and supplies during the pandemic.
        You made it possible to provide clean and safe drinking water to the community.
        We organized a cultural event to celebrate diversity and unity.
        The scholarship program enabled talented students to pursue higher education.
        Your support provided new sports equipment for the youth.
        The charity auction raised funds for medical equipment.
        We distributed warm clothing to homeless individuals during winter.
        Your contributions helped us build shelters for displaced families.
        The medical team conducted health check-ups in remote villages.
        Thanks to you, the school has new computers for digital learning.
        We provided support and counseling to survivors of domestic violence.
        Your generosity enabled us to plant trees for environmental conservation.
        The vocational training program empowered women with new skills.
        We distributed school supplies to children in need.
        Thanks to your donations, we provided hearing aids for the hearing-impaired.
        The community celebrated the opening of a new community garden.
        You made it possible to construct a playground for children with disabilities.
        We organized workshops on entrepreneurship for aspiring entrepreneurs.
        Your support enabled us to distribute food rations to hungry families.
        The charity run raised funds to support cancer patients.
        We conducted health camps to provide medical care to underserved areas.
        Thanks to you, we installed solar street lights for safety and security.
        The vocational training center equipped individuals with skills for employment.
        Your contributions helped us establish a women's empowerment center.
        We distributed school uniforms to ensure equal access to education.
        Thanks to your donations, we provided shelter to homeless individuals.
        The medical mission conducted surgeries for those in need.
        You made it possible to install a water filtration system in the village.
        We conducted awareness programs on environmental conservation.
        Your support enabled us to provide nutritional supplements to malnourished children.
        The charity event raised funds to sponsor education for orphans.
        We distributed winter kits to protect vulnerable families from the cold.
        Thanks to you, we provided medical supplies to health clinics.
        We organized a skills training workshop for unemployed youth.
        Your contributions supported the construction of a community hall.
        The vocational training program equipped individuals with new job skills.
        We distributed school bags and stationery to underprivileged students.
        Thanks to your donations, we provided eye care services to the elderly.
        The community celebrated the inauguration of a new vocational center.
        You made it possible to distribute relief supplies during emergencies.
        We conducted health education sessions to promote preventive care.
        Your support enabled us to provide access to clean drinking water.
        The charity bike ride raised funds for the education of underprivileged children.
        We distributed school shoes to children to attend school comfortably.
        Thanks to you, we installed solar-powered lights for community safety.
        We organized a workshop on women's health and hygiene.
        Your contributions helped us build playgrounds for children in need.
        The medical mission provided free healthcare to the elderly.
        You made it possible to establish a community library for learning.
        We distributed essential household items to families affected by disasters.
        Thanks to your donations, we conducted free medical camps in rural areas.
        The charity gala raised funds to support education initiatives.
    """

    #Generate 200 users
    
    unique_emails = set() #stores unique email addresses to ensure every email in the db is unique
    num_admins = 0
    num_donors = 0 
    num_charities = 0

    with open('user_credentials.txt', 'w') as file:
        for _ in range(200):
            email = None
            while not email or email in unique_emails:
                email = fake.email()
            password = fake.password()
            # Assign roles based on the counts: 140 donors, 10 admins, and 50 charities
            if num_donors < 140:
                role = 'donor'
                num_donors += 1
            elif num_admins < 10:
                role = 'admin'
                num_admins += 1
            else:
                role = 'charity'
                num_charities += 1

            username = fake.user_name()
            first_name = fake.first_name()
            last_name = fake.last_name()

            #Validate email format
            if '@' not in email or '.' not in email:
                continue

            unique_emails.add(email)

            hashed_password = generate_password_hash(password)
            new_user = User(
                email = email,
                password = hashed_password,
                role=role,
                user_name=username,
                first_name=first_name,
                second_name = last_name
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            # Write the user and password details to the text file
            file.write(f"User: {username}, Email: {email}, Password: {password}, Role: {role}\n")

            if num_donors == 140 and num_admins == 10 and num_charities == 50:
                break