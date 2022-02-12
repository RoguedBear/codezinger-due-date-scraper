#### Running times
- Lab tuesday: 8:30, 10:40
- Lab wednesday: 2:30, 4:40
- Lab Friday: 2:30, 4:40
- Sat: 7:30

#### Overview:
- Script Start
- Scrape Data off of Code ginger
- Insert data into "QuestionData" [table1]

- follow this logic before finally inserting
  ```md
  hashing:
  - generate a complete hash of all data points
  - if complete hash in database, then nothing changed
  - else if hash not in databse then:
    - check if (question + class) hash exists or not
      - if yes then either due date or question type changed
   - if that does not exist we have a new question
    ```
- process updated questions list
- process new questions list
- purge old data