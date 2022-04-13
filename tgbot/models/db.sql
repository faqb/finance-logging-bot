CREATE TABLE categories(
    id SERIAL PRIMARY KEY,
    en_category VARCHAR(255),
    uk_category VARCHAR(255),
    ru_category VARCHAR(255),
    picture VARCHAR(255) NOT NULL
);

CREATE TABLE aliases(
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id) NOT NULL UNIQUE,
    en_aliases TEXT [],
    uk_aliases TEXT [],
    ru_aliases TEXT []
);

CREATE TABLE consumption(
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id) NOT NULL,
    subcategory VARCHAR(255),
    amount INTEGER NOT NULL,
    created DATE NOT NULL
);

CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    lang VARCHAR(255) DEFAULT 'en' NOT NULL
);

CREATE TABLE lang(
    id SERIAL PRIMARY KEY,
    state VARCHAR(255),
    en_message TEXT,
    uk_message TEXT,
    ru_message TEXT
);

INSERT INTO categories
(
    en_category, uk_category, ru_category, picture
)
VALUES
    ('food', 'їжа', 'eда', U&'\+01F34E'),
    ('transport', 'транспорт', 'транспорт', U&'\+01F695'),
    ('other', 'інше', 'другое', U&'\+002705')
;

INSERT INTO subcategories
(
    category_id, en_subcategory, uk_subcategory, ru_subcategory
)
VALUES
    (1, ARRAY [ 'mac', 'coffee' ], ARRAY ['мак', 'кава' ], ARRAY [ 'мак', 'кофе' ]),
    (2, ARRAY ['subway', 'bus'], ARRAY ['метро', 'автобус' ], ARRAY ['метро', 'автобус'])
;

INSERT INTO aliases
(
    category_id, en_aliases, uk_aliases, ru_aliases
)
VALUES 
    (1, ARRAY [ 'food', 'products' ], ARRAY [ 'їжа', 'мак', 'продукти','харчування' ], ARRAY [ 'еда', 'мак', 'продукты', 'питание' ] ),
    (2, ARRAY [ 'transport', 'road', 'metro' ], ARRAY ['транспорт', 'дорога', 'метро', 'автобус' ], ARRAY [ 'транспорт', 'дорога', 'матро', 'автобус' ]),
    (3, ARRAY [ 'other' ], ARRAY [ 'інше' ], ARRAY [ 'другое', 'прочее' ])
;
