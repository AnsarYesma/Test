USE TabuBot$tgbot;
DROP TABLE rates;
DROP TABLE list;
DROP TABLE forms;
DROP TABLE users;

CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(100),
    registration_date DATE,
    last_active DATE
);

CREATE TABLE list (
    id INT,
    id_object INT,
    PRIMARY KEY (id, id_object),
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (id_object) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TABLE forms (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    year YEAR(4),
    gender VARCHAR(100),
    city VARCHAR(100),
    info VARCHAR(10000),
    image LONGBLOB,
    isActive BOOl,
    lastActive DATE,
    popularity INT,
    FOREIGN KEY (id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE rates (
    id INT,
    id_object INT,
    text_message VARCHAR(100),
    PRIMARY KEY (id, id_object),
    FOREIGN KEY (id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (id_object) REFERENCES users (id) ON DELETE CASCADE
);
