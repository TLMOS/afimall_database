CREATE TABLE store
(
  store_id SERIAL,
  "name" VARCHAR(255) NOT NULL,
  "floor" INT NOT NULL,
  working_hours VARCHAR(255) NOT NULL,
  website VARCHAR(255),
  description TEXT NOT NULL,
  phone VARCHAR(15),
  loyalty_program_member INT NOT NULL,
  PRIMARY KEY (store_id)
);

CREATE TABLE receipt
(
  store_id SERIAL,
  price REAL NOT NULL,
  receipt_nat_id BIGINT NOT NULL,
  PRIMARY KEY (receipt_nat_id),
  FOREIGN KEY (store_id) REFERENCES store(store_id)
);

CREATE TABLE promotion
(
  promotion_id SERIAL,
  date_from DATE NOT NULL,
  date_to DATE NOT NULL,
  description TEXT NOT NULL,
  store_id INT NOT NULL,
  PRIMARY KEY (promotion_id),
  FOREIGN KEY (store_id) REFERENCES store(store_id)
);

CREATE TABLE payment_category
(
  category_id SERIAL,
  "name" VARCHAR(50) NOT NULL,
  PRIMARY KEY (category_id)
);

CREATE TABLE store_category
(
  category_id SERIAL,
  "name" VARCHAR(255) NOT NULL,
  parent_id INT, 
  FOREIGN KEY (parent_id) REFERENCES store_category(category_id) , 
  PRIMARY KEY (category_id)
);

CREATE TABLE "rank"
(
  rank_id SERIAL,
  "name" VARCHAR(10) NOT NULL,
  PRIMARY KEY (rank_id)
);

CREATE TABLE store_to_category
(
  relation_id SERIAL,
  store_id INT NOT NULL,
  category_id INT NOT NULL,
  PRIMARY KEY (relation_id),
  FOREIGN KEY (store_id) REFERENCES store(store_id),
  FOREIGN KEY (category_id) REFERENCES store_category(category_id)
);

CREATE TABLE "user"
(
  user_id SERIAL,
  "name" VARCHAR(30) NOT NULL,
  car VARCHAR(50),
  income INT,
  birth_date DATE,
  phone VARCHAR(15) NOT NULL,
  balance INT NOT NULL,
  gender CHAR(1),
  rank_id INT NOT NULL,
  PRIMARY KEY (user_id),
  FOREIGN KEY (rank_id) REFERENCES "rank"(rank_id),
  UNIQUE (phone)
);

CREATE TABLE compliment
(
  compliment_id SERIAL,
  "cost" INT NOT NULL,
  "name" VARCHAR(255) NOT NULL,
  date_from DATE NOT NULL,
  date_to DATE NOT NULL,
  description TEXT NOT NULL,
  store_id INT NOT NULL,
  rank_id INT NOT NULL,
  PRIMARY KEY (compliment_id),
  FOREIGN KEY (store_id) REFERENCES store(store_id),
  FOREIGN KEY (rank_id) REFERENCES "rank"(rank_id)
);

CREATE TABLE payment
(
  payment_id SERIAL,
  "date" TIMESTAMP NOT NULL,
  amount INT NOT NULL,
  status VARCHAR(30) NOT NULL,
  user_id INT NOT NULL,
  category_id INT NOT NULL,
  receipt_nat_id BIGINT,
  compliment_id INT,
  PRIMARY KEY (payment_id),
  FOREIGN KEY (user_id) REFERENCES "user"(user_id),
  FOREIGN KEY (category_id) REFERENCES payment_category(category_id),
  FOREIGN KEY (receipt_nat_id) REFERENCES receipt(receipt_nat_id),
  FOREIGN KEY (compliment_id) REFERENCES compliment(compliment_id)
);

CREATE TABLE feedback_message
(
  message_id SERIAL,
  theme VARCHAR(255) NOT NULL,
  response_email VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  username VARCHAR(50) NOT NULL,
  status VARCHAR(30) NOT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (message_id),
  FOREIGN KEY (user_id) REFERENCES "user"(user_id)
);