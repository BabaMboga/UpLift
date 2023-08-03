from app import app
from models import db, User, Charity, Donation, Beneficiary, Inventory
from faker import Faker
import markovify
import random
from werkzeug.security import generate_password_hash
from datetime import timedelta

print("Seeding has started.")

fake = Faker()

with app.app_context():
    db.drop_all()
    db.create_all()

    def generate_random_text(text_corpus, max_length=255):
        text_model = markovify.Text(text_corpus)
        return text_model.make_sentence(max_length=max_length)
    
    #The below block of code will now be used to train the markov to generate good random story for beneficiary
    story_caption_corpus = """
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

    #List of charity names
    charity_names_list = [
        "Hopeful Hearts Charity","Brighter Futures Foundation","Helping Hands Organization","Compassionate Care Fund","Global Impact Initiative","Love and Light Charity","Bridge of Dreams Initiative","Empowering Communities Charity",
        "Wings of Compassion Trust","Together We Thrive Foundation","Reach for the Stars Charity","Embrace Diversity Organization","Seeds of Peace Foundation","Hand in Hand Relief Fund","Building Bridges Charity","Rays of Sunshine Charity",
        "Empowerment for All","Community Builders Charity","Caring Souls Society","Giving Back Foundation","Inspire Change Network","Bright Beginnings Foundation","Wings of Change Initiative","Empowering Tomorrow's Leaders",
        "Dream Big Charity","Unity in Diversity Foundation","Heal the World Mission","Rise Up Together Foundation","Kindness Matters Association","United in Hope Foundation","Open Hearts Community","Breaking Barriers Foundation",
        "Share the Love Charity","Changing Lives Project","One Step at a Time Charity","Open Arms Support Group","Rays of Hope Foundation","Care and Share Initiative","Change the World Organization","Wings of Hope Mission",
        "Embracing Humanity Foundation","Shine Your Light Charity","Uplift the World Association","New Horizons Charity","Better Tomorrow Project","Helping Hearts Alliance","Rise Above Adversity Charity","Light of Love Foundation",
        "Bridge the Gap Charity","Infinite Possibilities Trust"
    ]

    with open('user_credentials.txt', 'w') as file:
        while num_donors < 140:            
            email = fake.email()
            password = fake.password()
            username = fake.user_name()

             #Validate email format
            if '@' not in email or '.' not in email:
                continue
            if email in unique_emails:
                continue

            unique_emails.add(email)

            hashed_password = generate_password_hash(password)
            new_user = User(
                email = email,
                password = hashed_password,
                role='donor',
                user_name=username,
                official_name=fake.name()
            )

            db.session.add(new_user)
            db.session.commit()

            # Write the user and password details to the text file
            file.write(f"User: {username}, Email: {email}, Password: {password}, Role: {new_user.role}\n")

            num_donors += 1

        while num_admins< 10:
            email = fake.email()
            password = fake.password()
            username = fake.user_name()

             #Validate email format
            if '@' not in email or '.' not in email:
                continue
            if email in unique_emails:
                continue

            unique_emails.add(email)

            hashed_password = generate_password_hash(password)
            new_user = User(
                email = email,
                password = hashed_password,
                role='admin',
                user_name=username,
                official_name=fake.name()
            )

            db.session.add(new_user)
            db.session.commit()

            # Write the user and password details to the text file
            file.write(f"User: {username}, Email: {email}, Password: {password}, Role: {new_user.role}\n")

            num_admins += 1

        while num_charities < 50:
            email = fake.email()
            password = fake.password()
            username = fake.user_name()

             #Validate email format
            if '@' not in email or '.' not in email:
                continue
            if email in unique_emails:
                continue

            unique_emails.add(email)

            hashed_password = generate_password_hash(password)
            new_user = User(
                email = email,
                password = hashed_password,
                role='charity',
                user_name=username,
                official_name=charity_names_list.pop()
            )

            db.session.add(new_user)
            db.session.commit()

            # Write the user and password details to the text file
            file.write(f"User: {username}, Email: {email}, Password: {password}, Role: {new_user.role}\n")

            num_charities += 1


            if num_donors == 140 and num_admins == 10 and num_charities == 50:
                break

    print("Users successfully seeded")

    #The below code will now be used to train the makovify to generate comprehendable descriptions for charities
    description_caption_corpus="""
        Hopeful Hearts Charity embraces hope for a brighter future.
        Brighter Futures Foundation empowers individuals for a brighter tomorrow.
        Helping Hands Organization extends helping hands to those in need.
        Compassionate Care Fund provides compassionate care to all.
        Global Impact Initiative strives for a positive global impact.
        Empowerment for All empowers everyone to reach their full potential.
        Community Builders Charity builds strong communities through unity.
        Caring Souls Society cares for the souls of those it serves.
        Giving Back Foundation believes in giving back to society.
        Inspire Change Network inspires positive change in the world.
        Dream Big Charity encourages everyone to dream big.
        Unity in Diversity Foundation celebrates the beauty of diversity.
        Heal the World Mission works to heal the world with kindness.
        Rise Up Together Foundation rises together for a common cause.
        Kindness Matters Association spreads kindness wherever it goes.
        Share the Love Charity shares love and compassion with all.
        Changing Lives Project changes lives through transformative projects.
        One Step at a Time Charity takes one step at a time for progress.
        Open Arms Support Group welcomes all with open arms.
        Rays of Hope Foundation brings rays of hope to those in need.
        Love and Light Charity shines the light of love on all.
        Bridge of Dreams Initiative bridges dreams and reality.
        Empowering Communities Charity empowers communities for growth.
        Wings of Compassion Trust spreads wings of compassion far and wide.
        Together We Thrive Foundation thrives together as a united force.
        Reach for the Stars Charity encourages individuals to reach for their dreams.
        Embrace Diversity Organization embraces the beauty of diversity.
        Seeds of Peace Foundation plants seeds of peace in the world.
        Hand in Hand Relief Fund offers a helping hand to those in crisis.
        Building Bridges Charity builds bridges for better connections.
        Wings of Hope Mission brings hope to those in despair.
        Embracing Humanity Foundation embraces the humanity in all of us.
        Shine Your Light Charity encourages everyone to shine their light.
        Uplift the World Association aims to uplift the world with positivity.
        New Horizons Charity opens doors to new horizons for all.
        Better Tomorrow Project works for a better tomorrow for everyone.
        Helping Hearts Alliance aligns hearts to help those in need.
        Bright Beginnings Foundation starts bright beginnings for a better future.
        Wings of Change Initiative brings positive change like the wind.
        Empowering Tomorrow's Leaders empowers the leaders of tomorrow.
        Rays of Sunshine Charity spreads rays of sunshine to all.
        United in Hope Foundation stands united in the hope for a better world.
        Open Hearts Community embraces everyone with open hearts.
        Breaking Barriers Foundation breaks barriers for progress.
        Care and Share Initiative cares and shares with those less fortunate.
        Change the World Organization strives to change the world for the better.
        Rise Above Adversity Charity rises above adversity with strength.
        Light of Love Foundation shines the light of love on all it serves.
        Bridge the Gap Charity bridges the gap for those in need.
        Infinite Possibilities Trust believes in the infinite possibilities of change.
        Embrace the Journey Charity embraces the journey of growth and transformation.
        Empower Minds Foundation empowers minds with knowledge and education.
        Hope in Action Organization turns hope into action to make a real impact.
        Together We Soar Foundation believes in soaring together towards a brighter future.
        Changing Tides Initiative brings positive change like changing tides in the ocean.
        United Hearts Charity unites hearts with love and compassion for all.
        Bridge to Success Foundation builds bridges to lead individuals to success.
        Rays of Compassion Mission spreads rays of compassion and empathy to all.
        Dreams to Reality Charity turns dreams into reality for those in need.
        Open Minds Society promotes open minds and acceptance in society.
        Empowering Hands Association empowers individuals through helping hands.
        Hearts United Fund unites hearts and resources to create positive change.
        Embrace Diversity Foundation embraces the beauty of diversity in humanity.
        Reach for the Skies Charity encourages individuals to reach for the skies.
        Steps Towards Hope Initiative takes steps towards bringing hope to all.
        Rising Together Foundation rises together as a community for collective progress.
        Light the Path Charity lights the path for those in search of guidance.
        Caring Connections Organization fosters caring connections within communities.
        Change-makers Alliance brings change-makers together for a common cause.
        Building Dreams Together Initiative builds dreams together for a better world.
        Hopeful Horizons Mission looks forward to hopeful and bright horizons.
        Empowerment Waves Charity creates waves of empowerment in society.
        Seeds of Change Foundation plants seeds of positive change for all.
        Embrace the Challenge Organization embraces challenges with determination.
        Empowering Voices Association empowers voices to be heard and valued.
        Light the World Foundation seeks to light the world with compassion and love.
        United in Kindness Mission stands united in spreading kindness far and wide.
        Reach Out and Care Initiative reaches out to those in need with care and support.
        Rays of Inspiration Fund brings rays of inspiration to individuals' lives.
        Hearts in Harmony Charity aims for hearts to beat in harmony with each other.
        Bridge of Opportunities Organization builds bridges of opportunities for all.
        Embrace the Possibilities Foundation embraces the endless possibilities of change.
        Together We Serve Charity believes in serving together for a greater purpose.
        Changing Lives Together Initiative is committed to changing lives together.
        Hopeful Hearts United brings together hopeful hearts to make a difference.
        Empowerment Pathways Fund paves pathways to empowerment for all.
        Seeds of Hope Initiative plants seeds of hope for a brighter tomorrow.
        Embrace the Journey Together Foundation embraces the journey together as one.
        Rise Above and Shine Charity encourages individuals to rise above and shine.
        Caring Hands Network extends caring hands to those in need.
        Change Starts Within Organization believes change starts within oneself.
        Building Together for Tomorrow Initiative builds together for a better tomorrow.
        Hearts Full of Hope Charity has hearts full of hope for those it serves.
        United by Compassion Mission stands united by the power of compassion.
        Reach for Dreams Foundation encourages individuals to reach for their dreams.
        Rays of Support Association offers rays of support to those in distress.
        Light the Way Initiative lights the way for those in search of a path.
        Hearts in Harmony Together Foundation believes in harmony through togetherness.
        Bridging the Divide Charity bridges the divide between communities.
        Empower and Inspire Organization aims to empower and inspire all.
    """

    print("Users Successfully seeded")

    for _ in range(50):
        charity_name = charity_names_list.pop()
        description = generate_random_text(description_caption_corpus)
        status = random.choice([True, False])
        amount_received = random.randint(1000, 1000000)

        new_charity = Charity(
            name=charity_name,
            description = description,
            status=status,
            amount_received=amount_received
        )

        db.session.add(new_charity)
        db.session.commit()

    print("Charities sucessfully seeded")

    # creating 200 fake donations

    users = User.query.filter_by(role='donor').all()
    charities = Charity.query.filter_by(status = True).all()
    for _ in range(200):
        donor = random.choice(users)
        charity = random.choice(charities)
        donation = Donation(
            donor_id = donor.id,
            charity_id = charity.charity_id,
            amount = random.uniform(10,1000),
            donation_date = fake.date_time_this_year(),
            is_anonymous = random.choice([True, False]),
            schedule_frequency= random.choice(["none","weekly","monthly"]),
            schedule_start_date = None,
            schedule_end_date=None
            

        )
        # Set schedule_start_date and schedule_end_date 
        if donation.schedule_freequency in ["weekly", "monthly"]:
            donation.schedule_start_date = fake.date_time_this_year()

            if donation.schedule_frequency == "weekly":
                donation.schedule_end_date = donation.schedule_start_date + timedelta(weeks=4)
            else:
                donation.schedule_end_date = donation.schedule_start_date + timedelta(months=4)


        db.session.add(donation)
        db.session.commit()

    print("Donations successfully seeded")

    # Create 200 beneficiaries
    for _ in range(200):
        charity= random.choice(charities)
        beneficiary = Beneficiary(
            charity_id = charity.charity_id,
            beneficiary_name = fake.name(),
            story = generate_random_text(story_caption_corpus)
        )
        db.session.add(beneficiary)
        db.session.commit()

    print("Benefeciaries successfully seeded")

    #create 100 inventory entries

    #list of inventory items
    inventory_items = [
        "Rice", "Beans", "Canned goods", "Flour", "Cooking oil", "Pasta", "Soap", "Shampoo", "Toothpaste", "Toothbrushes",
        "Sanitary pads", "Diapers", "T-shirts", "Pants", "Shoes", "Blankets", "Bed sheets", "School bags", "Notebooks",
        "Pens and pencils", "Stationery items", "First aid kits", "Bandages", "Over-the-counter medicines", "Water filters",
        "Water purification tablets", "Cooking utensils", "Plates and cutlery", "Cooking stoves", "Solar-powered lights",
        "Mobile phones", "Chickens", "Goats", "Seeds", "Computers", "Projectors", "Books and educational materials",
        "Mosquito nets", "Sleeping mats", "Flashlights", "Batteries", "Sewing machines", "Clothing fabric", "Raincoats",
        "Solar panels", "Hand tools", "Sewing supplies", "Farming tools", "Vegetable seeds", "Educational toys"
    ]

    for _ in range(100):
        charity = random.choice(charities)
        item_name = random.choice(inventory_items)
        quantity = random.randint(1, 100)
        date_sent = fake.date_time_this_year()

        inventory = Inventory(
            charity_id = charity.charity_id,
            item_name = item_name,
            quantity = quantity,
            date_sent = date_sent
        )

        db.session.add(inventory)
        db.session.commit()

    print("Inventories successfully seeded")
    print("Finished seeding")