# **Quantum Query Comparator [Q2C]- Transcending textual boundaries, using semantic spheres**

## **Introduction**

 ---

<p style="text-align: center;">
  <img src="/resources/_sources/_img/_logo.png"  alt="logo"/>
</p>

Quantum Query Comparator (Q2C) is an innovative NLP chatbot designed to understand and compare the semantic essence of
user requests with a predefined question base. Instead of simple text matching, Q2C deepens the meaning of each query,
providing an accurate, contextually meaningful response each time.

## **Week I progress**

 ---

### Agenda:

- Road map
- Team formation
- Data collection

### Problem statement

Humor is inherently subjective, and what one person finds funny, another might not. But with machine learning and deep
learning, we can try to model some patterns of humor. To successfully implement the project, we created road-map:

- [x] *Preliminary Planning & Research:*
    - Team formation.
    - Identify the project's objectives and scope.
    - Research existing humor datasets and potential sources.

- [x] *Data Collection & Processing:*
    - Collect a more extensive set of questions and their paraphrases to train similarity models
    - Data cleaning: removing duplicates, correcting typos, etc.
    - Split the data into training, validation, and test sets.

- [ ] *Model Selection & Prototyping:*
    - Choose baseline models (TF-IDF, Count Vectorizer)
    - Experiment with advanced models (Word Embeddings, BERT, RoBERTa)
    - Implement similarity scoring mechanisms (cosine similarity, Euclidean distance)

- [ ] *Training & Fine-tuning:*
    - Train the selected models using the training dataset
    - Fine-tune the models using transfer learning on the validation dataset

- [ ] *Evaluation & Testing:*
    - Evaluate the models using the test dataset
    - Calculate precision, recall, F1-score for similarity thresholding
    - Incorporate user feedback for iterative improvements

- [ ] *Deployment & Scalability:*
    - Deploy the model on a scalable platform (Telegram)
    - Monitor usage and ensure uptime and performance metrics are met

At the moment, *Preliminary Planning & Research* is fully completed, and work on the second point of road-map.

### Team Formation

The team was created on the basis of each member’s stack. Some additional roles had to be shared among the participants,
due to the small size of the team. You can see the table below with all members and their contacts:

| **Team Member** | Elina Akimchenkova                  | Ruslan Abdullin                                | Anatoliy Pushkarev                                |
|-----------------|-------------------------------------|------------------------------------------------|---------------------------------------------------|
| **Telegram ID** | [@akmchnkv](https://t.me/akmchnkv)  | [@Fliegende_Rehe](https://t.me/Fliegende_Rehe) | [@anatoliy_pus](https://t.me/anatoliy_pus)        |
| **Email**       | e.akimchenkova@innopolis.university | ru.abdullin@innopolis.university               | a.pushkarev@innopolis.university                  |
| **Role**        | Data engineer                       | ML engineer                                    | Quality Assurance Engineer<br/>Software Developer |

### Data collection

We started building data-sets using several sources:

- Public datasets: Kaggle Quora Dataset Release: Question Pairs
- Web scraping

Since we don’t have much time to collect data. Now we try to use special techniques to augment the data:

- Back-translation (translate anecdotes to another language and then translate it back to original).
- Paraphrasing tools (use tools to rephrase the anecdotes).

## **Useful links**

 ---

- [GitHub link](https://t.me/akmchnkv)  
