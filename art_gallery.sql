create database mydb2;
use mydb2;

create table artwork(
	id int primary key,
	category varchar(25),
    name varchar(100),
    product_path varchar(50),
    artist_name varchar(50),
    year int,
    size varchar(250),
    price float,
    description varchar(500)
);

insert into artwork values
(1,'Landscape', 'Vivid','static/images/painting_1.jpg','Arjun Mehta', 2019, '24"x30"', 400,'A striking landscape with bold, colorful skies and lush greenery, evoking a sense of optimism and vibrancy.'),
(2,'Landscape', 'Seaside Retreat','static/images/painting_2.jpg','Arjun Mehta', 2020, '24"x30"', 600,'A serene landscape with towering mountains, a calm sea, and a quaint house beside a tree, evoking tranquility.'),
(3,'Landscape', 'Mountain Horizon','static/images/painting_3.jpg','Arjun Mehta', 2020, '24"x30"', 500,'A bold, sweeping landscape sketch that highlights towering mountain peaks against a serene sky, evoking a sense of vastness.'),
(4,'Landscape', 'River Through the Forest','static/images/painting_4.jpg','Priya Nair', 2022, '30"x30"', 400,'A peaceful river winding through a dense forest, with trees reflecting in the still water.'),
(5,'Landscape', 'Woodland Stream','static/images/painting_5.jpg','Priya Nair', 2020, '24"x30"', 700,'A clear river flows gently through an ancient forest, offering a sense of calm and connection to nature.'),
(6,'Landscape', 'Mountain Escape','static/images/painting_6.jpg','Priya Nair', 2020, '24"x30"', 600,'A peaceful river winding through a dense forest, with trees reflecting in the still water.'),
(7,'Landscape', 'Golden Dusk','static/images/painting_7.jpg','Priya Nair', 2017, '24"x30"', 700,'A breathtaking landscape with the warm hues of a sunset casting a golden glow over rolling hills and a tranquil lake.'),
(8,'Portrait', 'Serenity in Silence','static/images/portrait_1.jpg','Priya Nair', 2018, '30"x30"', 700,'A captivating portrait that emphasizes calm and introspection. Subtle brushstrokes and soft tones bring out the peaceful expression of the subject, creating a soothing atmosphere. '),
(9,'Sketches', 'The Forgotten Ride','static/images/sketch_1.jpg','Arjun Mehta', 2023, '15"x34"', 300,'A nostalgic sketch featuring an old car resting in a rustic shed, surrounded by overgrown vines and the soft light filtering through the wooden slats.'),
(10,'Sketches', 'River\'s Path','static/images/sketch_2.jpg','Arjun Mehta', 2023, '15"x34"', 300,'A peaceful sketch of a winding river cutting through the land, with trees and rocks lining its banks, evoking a sense of serenity and flow.'),
(11,'Sketches', 'The Forgotten Ride','static/images/sketch_3.jpg','Arjun Mehta', 2023, '15"x34"', 300,'A solitary car rusting in the grass, surrounded by overgrown trees and forgotten memories.'),
(12,'Sketches', 'Hilltop Haven','static/images/sketch_4.jpg','Meera Kapoor', 2023, '15"x34"', 500,'This tranquil sketch depicts a house nestled on a hillside, surrounded by lush greenery and towering trees. The serene landscape evokes a sense of calm, with sweeping views of the valley below.'),
(13,'Sketches', 'Stream\'s Journey','static/images/sketch_5.jpg','Meera Kapoor', 2021, '22"x34"', 400,'A delicate sketch showing a winding stream that cuts through a forest, its crystal-clear waters flowing over smooth rocks, reflecting the surrounding greenery.'),
(14,'Abstract', 'Whispers of the Earth','static/images/pottery_1.jpg','Ravi Deshpande', 2022, '15"x25"', 800, 'A ceramic sculpture with smooth, flowing curves and textured surfaces, symbolizing the ancient bond between earth and fire.'),
(15,'Abstract', 'Fireside Vessel','static/images/pottery_2.jpg','Ravi Deshpande', 2023, '25"x24"', 900,'A warm, rustic pottery piece, capturing the essence of a crackling fire and the warmth it provides, with intricate patterns inspired by nature.'),
(16,'Abstract', 'Ceramic Dream','static/images/pottery_3.jpg','Ravi Deshpande', 2022, '15"x24"', 700, 'A stunning pottery creation with soft, muted glazes that evoke a dreamlike atmosphere, blending organic forms with modern elegance.'),
(17,'Abstract', 'Whispers of Clay','static/images/pottery_4.jpg','Ravi Deshpande', 2023, '14"x24"', 700,'A beautifully crafted pottery piece, showcasing delicate, flowing curves. '),
(18,'Abstract', 'Stellar Drift','static/images/space_1.jpg','Anjali Sharma', 2022, '25"x20"', 700,' Bold colors and dynamic shapes evoke the vast, mysterious beauty of the cosmos, inviting the viewer to drift into an otherworldly dream.'),
(19,'Abstract', 'Cosmic Reverie','static/images/space_2.jpg','Anjali Sharma', 2021, '14"x24"', 700,'An abstract depiction of the cosmos, with stars and cosmic dust blending into one fluid motion.'),
(20,'Abstract', 'Storm on the Horizon','static/images/abstract_1.jpg','Anjali Sharma', 2023, '14"x24"', 700, 'A bold abstract painting portraying an impending storm, with strokes of rich oranges, reds, and yellows symbolizing nature’s intense energy.'),
(21,'Abstract', 'Vibrant Chaos','static/images/abstract_2.jpg','Anjali Sharma', 2024, '23"x20"', 1030,'A chaotic yet expressive sketch where bold strokes in shades of red, orange, and yellow come together in a flowing, abstract composition.'),
(22,'Abstract', 'Crimson Drift','static/images/abstract_3.jpg','Anjali Sharma', 2023, '14"x24"', 1930,'An abstract sketch with swirling lines and shapes, evoking the movement of heat waves in a rich crimson hue.');

create table events(
	event_id int primary key,
	event_name varchar(256),
    event_date date,
    description varchar(500)
);

alter table events
add column event_img varchar(256);

create table artists(
	artist_id int primary key,
    artist_name varchar(256),
	hails_from varchar(256),
    description varchar(500),
    artist_img varchar(256)
);

create table later_events(
	event_id int primary key,
	event_name varchar(256),
    event_date date,
    description varchar(500),
    event_img varchar(256)
);

create table registered_users(
	user_id int auto_increment primary key,
	fname varchar(256),
    lname varchar(256),
    email varchar(256),
    password varchar(256),
    c_password varchar(256),
    phone varchar(15),
    address varchar(500)
);

select * from registered_users;

drop table later_events;

SELECT * 
FROM mydb2.events
WHERE event_date BETWEEN CURRENT_DATE() AND '2025-01-30';

SELECT * 
FROM mydb2.events
WHERE event_date>'2025-01-30';

create table customer_query(
	name varchar(50),
    email varchar(100),
    message varchar(500)
);

SELECT event_name FROM mydb2.events WHERE event_date BETWEEN CURRENT_DATE() AND '2025-01-30' LIMIT 2;

create table orders(
id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE,
    product_name VARCHAR(255),
    price DECIMAL(10, 2),
    status VARCHAR(50),
    user_email VARCHAR(255)
);
drop table event_users;

create table event_users(
	user_id int auto_increment primary key,
	fname varchar(256),
    lname varchar(256),
    email varchar(256),
    phone varchar(15),
    event varchar(100)
);

insert into artwork values
(23,'Photography', 'Desert Oasis Classic','static/images/photography_1.jpg','Anjali Sharma', 2020, '14"x24"', 700,'A timeless white car parked beneath a lone tree in an arid, dramatic desert landscape.'),
(24,'Photography', 'Abandoned Serenity','static/images/photography_2.jpg','Arjun Mehta', 2021, '14"x24"', 800,'A weathered, solitary wooden house stands resilient amidst a vast and empty plain.'),
(25,'Photography', 'Vintage Charm on the Trail','static/images/photography_3.jpg','Anjali Sharma', 2020, '14"x24"', 900,'A radiant red vintage car parked along a dirt path with lush greenery in the background.'),
(26,'Photography', 'Timeless Gaze','static/images/photography_4.jpg','Priya Nair', 2023, '14"x24"', 700,'A black-and-white portrait of a woman lost in thought, her eyes fixed on the infinite, capturing a moment of quiet introspection.'),
(27,'Photography', 'Echo of Resilience','static/images/photography_5.jpg','Ravi Deshpande', 2020, '14"x24"', 800,'A solitary withered tree stands as a stark reminder of endurance amidst the passage of time.');

drop table event_users;

create table registered_users(
	user_id int auto_increment primary key,
	fname varchar(256),
    lname varchar(256),
    email varchar(256),
    password varchar(256),
    c_password varchar(256),
    phone varchar(15),
    address varchar(500)
);

CREATE TABLE cart (
    user_id INT,
    user_name VARCHAR(50),
    product_id INT,
    product_name VARCHAR(100),
    price FLOAT
);

drop table customer_query;

create table customer_query(
	name varchar(50),
    email varchar(100),
    message varchar(500),
    status varchar(50)
);

create table admin(
	email varchar(100),
    password varchar(10)
);

insert into admin values
('admin@gmail.com', 'admin123');

insert into cart values (1,"A",2,"ABC",700), (1,"A",3,"DEF",600), (1,"A",4,"EFG",700);

SELECT SUM(price) AS total_price FROM cart WHERE user_id=1;

drop table customer_query;

create table customer_query(
	query_id int primary key auto_increment,
	name varchar(50),
    email varchar(100),
    message varchar(500),
    status varchar(50)
);