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

- age 대신 birthdate를 저장하였다.

## API 명세

1. 회원 추가

   - Endpoint: /member
   - Method: POST
   - Request Body: (Example)

   ```json
   {
     "name": "John De",
     "birthDate": "2014-01-05T16:59:33+00:00",
     "role": "admin"
   }
   ```

   - Description: 새로운 사용자를 추가합니다.
   - Response: (Example)

   ```json
   {
     "data": [
       {
         "id": "655c0845cf243a936b29d515",
         "name": "John De",
         "birthDate": "2014-01-05T16:59:33Z",
         "role": "admin"
       }
     ],
     "code": 201,
     "message": "Member added successfully."
   }
   ```

2. 전체 사용자 조회 (Example)

   - Endpoint: /member
   - Method: GET
   - Description: 전체 사용자 목록을 조회합니다.
   - Response: (Example)

   ```json
   {
     "data": [
       [
         {
           "id": "655b220be896c1e19d6ae8ab",
           "name": "John Doe",
           "birthDate": "1999-01-05T16:59:33",
           "role": "admin"
         },
         {
           "id": "655b2265b2a7ed6b8c762149",
           "name": "John De",
           "birthDate": "2014-01-05T16:59:33Z",
           "role": "admin"
         },
         {
           "id": "655c0845cf243a936b29d515",
           "name": "John De",
           "birthDate": "2014-01-05T16:59:33Z",
           "role": "admin"
         }
       ]
     ],
     "code": 200,
     "message": "Members data retrieved successfully"
   }
   ```

3. 특정 사용자 조회

   - Endpoint: /member/{member_id}
   - Method: GET
   - Parameters:
     - member_id: 조회하고자 하는 사용자의 고유한 ID
   - Description: 특정 ID를 가진 사용자의 정보를 조회합니다.
   - Response: (Example)

   ```json
   {
     "data": [
       {
         "id": "655b220be896c1e19d6ae8ab",
         "name": "John Doe",
         "birthDate": "1999-01-05T16:59:33",
         "role": "admin"
       }
     ],
     "code": 200,
     "message": "Member data retrieved successfully"
   }
   ```

4. 사용자 정보 업데이트

   - Endpoint: /member/{member_id}
   - Method: PUT
   - Parameters:
     - member_id: 업데이트하고자 하는 사용자의 고유한 ID
   - Request Body: (Example)

   ```json
   {
     "name": "John An",
     "birthDate": "2014-01-05T16:59:33+00:00",
     "role": "student"
   }
   ```

   - Description: 특정 ID를 가진 사용자의 정보를 업데이트합니다.
   - Response: (Example)

   ```json
   {
     "data": [
       {
         "id": "655b2265b2a7ed6b8c762149",
         "name": "John An",
         "birthDate": "2014-01-05T16:59:33",
         "role": "student"
       }
     ],
     "code": 200,
     "message": "Member data updated successfully"
   }
   ```

5. 사용자 회원 탈퇴
   - Endpoint: /member/{member_id}
   - Method: DELETE
   - Parameters:
     - member_id: 삭제하고자 하는 사용자의 고유한 ID
   - Description: 특정 ID를 가진 사용자를 회원 탈퇴 처리합니다.
   - Response: (Example)
   ```json
   {
     "data": ["Member with ID: 655b220be896c1e19d6ae8ab removed"],
     "code": 200,
     "message": "Member deleted successfully"
   }
   ```

## Lvl0. DB 대신 단순히 Dict만 사용해 구현

FastAPI를 통해 빠르게 API 구현이 가능하다.

[해당 구현 Commit](https://github.com/kunheekimkr/MO4E-DevKor/commit/d689ddabe1c39171aa7dfbc11c50ab471bbc19f9)

## Lvl1. DB를 사용해 구현

MongoDB를 사용해 구현해 보았다. 변경점으로는 파일 모듈화를 진행하였고, \_id를 사용해 각 멤버 시 자동으로 고유 id가 부여된다.
[해당 구현 Commit](https://github.com/kunheekimkr/MO4E-DevKor/commit/5a58e1c454e9b2d0662c4cca1fa628375b48c3cb)

[Docs](./images/swagger.png)

ToDo:

- [v] BirthDate DateTime Type검사 추가
- [v] HTTP 응답코드 제대로 처리
- [ ] UI 구현
- [ ] Dockerize
