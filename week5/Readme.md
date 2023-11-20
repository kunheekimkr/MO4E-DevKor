# Week 5: FastAPI

## Task

회원 관리 시스템을 만들려고 합니다.
회원은 id(string), name(string), age(int), role(string)이라는 property를 가지고 있습니다.
role은 admin과 student 두가지로 구분됩니다.
다음의 기능이 구현되어야 합니다.

1. 전체 사용자 조회
2. 사용자의 id를 이용해서 특정 사용자 조회
3. 특정 id를 가진 사용자 정보를 업데이트
4. 특정 id를 가진 사용자의 회원 탈퇴

(+ 추가) 사용자 추가

## API 명세

1. 사용자 추가

   - Endpoint: /users
   - Method: POST
   - Request Body: (Example)

   ```json
   {
     "name": "New User",
     "age": 20,
     "role": "student"
   }
   ```

   - Description: 새로운 사용자를 추가합니다.
   - Response: (Example)

   ```json
   {
     "id": 1,
     "name": "New User",
     "age": 20,
     "role": "student"
   }
   ```

2. 전체 사용자 조회 (Example)

   - Endpoint: /users
   - Method: GET
   - Description: 전체 사용자 목록을 조회합니다.
   - Response: (Example)

   ```json
   [
     {
       "id": 1,
       "name": "New User",
       "age": 20,
       "role": "student"
     },
     {
       "id": 2,
       "name": "New User2",
       "age": 25,
       "role": "admin"
     }
   ]
   ```

3. 특정 사용자 조회

   - Endpoint: /users/{user_id}
   - Method: GET
   - Parameters:
     - user_id: 조회하고자 하는 사용자의 고유한 ID
   - Description: 특정 ID를 가진 사용자의 정보를 조회합니다.
   - Response: (Example)

   ```json
   {
     "id": 1,
     "name": "New User",
     "age": 20,
     "role": "student"
   }
   ```

4. 사용자 정보 업데이트

   - Endpoint: /users/{user_id}
   - Method: PUT
   - Parameters:
     - user_id: 업데이트하고자 하는 사용자의 고유한 ID
   - Request Body: (Example)

   ```json
   {
     "name": "Updated Name",
     "age": 25,
     "role": "admin"
   }
   ```

   - Description: 특정 ID를 가진 사용자의 정보를 업데이트합니다.
   - Response: (Example)

   ```json
   {
     "id": 1,
     "name": "Updated Name",
     "age": 25,
     "role": "admin"
   }
   ```

5. 사용자 회원 탈퇴
   - Endpoint: /users/{user_id}
   - Method: DELETE
   - Parameters:
     - user_id: 삭제하고자 하는 사용자의 고유한 ID
   - Description: 특정 ID를 가진 사용자를 회원 탈퇴 처리합니다.
   - Response: (Example)
   ```json
   {
     "message": "User with id 1 has been deleted"
   }
   ```

## Lvl0. DB 대신 단순히 Dict만 사용해 구현

FastAPI를 통해 빠르게 API 구현이 가능하다.

[devkor_user_management.py](https://github.com/kunheekimkr/MO4E-DevKor/commit/d689ddabe1c39171aa7dfbc11c50ab471bbc19f9)

## Lvl1. DB를 사용해 구현

MongoDB를 사용해 구현해 보았다. 변경점으로는 파일 모듈화를 진행하였고, \_id를 사용해 각 멤버 시 자동으로 고유 id가 부여된다.
[해당 구현 Commit](https://github.com/kunheekimkr/MO4E-DevKor/commit/7f9438e1f5c16978089658c514d39a612733ac06)

ToDo:

- [v] BirthDate DateTime Type검사 추가
- [ ] 일부 value 만 update 가능하도록 수정
- [ ] HTTP 응답코드 제대로 처리
- [ ] id가 아닌 다른 property로 조회 가능하도록 수정
- [ ] UI 구현
- [ ] Dockerize
