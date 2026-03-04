// Task 2: use database
use bookstore

// Task 3: insert first author
db.authors.insertOne({
  "name": "Jane Austen",
  "nationality": "British",
  "bio": {
    "short": "English novelist known for novels about the British landed gentry.",
    "long": "Jane Austen was an English novelist whose works critique and comment upon the British landed gentry at the end of the 18th century. Her most famous novels include Pride and Prejudice, Sense and Sensibility, and Emma, celebrated for their wit, social commentary, and masterful character development."
  }
})

// Task 4: update to add birthday
db.authors.updateOne(
  { name: "Jane Austen" },
  { $set: { birthday: "1775-12-16" } }
)

// Task 5: insert four more authors
db.authors.insertMany([
  {
    name: "Virginia Woolf",
    nationality: "British",
    birthday: "1882-01-25",
    bio: {
      short: "English writer and modernist pioneer.",
      long: "Virginia Woolf was an English writer known for modernist novels and essays, experimenting with stream-of-consciousness narrative techniques."
    }
  },
  {
    name: "Chinua Achebe",
    nationality: "Nigerian",
    birthday: "1930-11-16",
    bio: {
      short: "Nigerian novelist, poet, and critic.",
      long: "Chinua Achebe was a Nigerian writer whose work explores the impacts of colonialism and cultural change, widely known for Things Fall Apart."
    }
  },
  {
    name: "Haruki Murakami",
    nationality: "Japanese",
    birthday: "1949-01-12",
    bio: {
      short: "Japanese novelist known for surreal, contemporary fiction.",
      long: "Haruki Murakami is a Japanese writer whose works often blend everyday realism with dreamlike elements, exploring themes of loneliness and identity."
    }
  },
  {
    name: "Gabriel García Márquez",
    nationality: "Colombian",
    birthday: "1927-03-06",
    bio: {
      short: "Colombian novelist associated with magical realism.",
      long: "Gabriel García Márquez was a Colombian writer whose novels popularized magical realism, including One Hundred Years of Solitude."
    }
  }
])

// Task 6: total count
db.authors.countDocuments({})

// Task 7: British authors, sorted by name
db.authors.find({ nationality: "British" }).sort({ name: 1 })