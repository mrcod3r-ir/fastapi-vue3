> See the dev branch for the latest code

# Student course selection system

## preview

- 🎉🎉🎉Thanks to [**wendingming**](https://gitee.com/wendingming) for [<font color="red">Preparation for project deployment</font>](https://gitee .com/zxiaosi/fast-api/issues/I4V6WV)
- 🎉🎉🎉Thanks to [**dreamrise**](https://gitee.com/dreamrise) for [<font color="red">Introduction to running configuration</font>](https://gitee.com /zxiaosi/fast-api/issues/I56HPN)

## Install

- **Backend installation**: [FastAPI](https://gitee.com/zxiaosi/fast-api/tree/master/backend#installation) (code reference[CharmCode](https://www.charmcode. cn/category/FastAPI?page=1))
- **Front-end installation**: [Vue3+Ts](https://gitee.com/zxiaosi/fast-api/tree/master/frontend#installation) (code reference[Vue-Manage-System](https:/ /github.com/lin-xin/vue-manage-system))

## Version

- `1.0` The addition, deletion and modification of test data has been completed
- `1.1` The addition, deletion and modification of the department table has been completed (see `Information table`)
- `1.2` Optimization of dashboard information on home page
- `1.3` Preliminary completion of adding, deleting, modifying and checking the department table
- `1.4` clean up code
- `1.5` added teacher table
- `1.6` added student table, course table, course selection table
- `1.7` refactored front-end code
- `1.8` package components, remove redundant code
- `1.9` custom table component
- `2.0` deployment project
- `2.1` refactored FastAPI
- `2.2` Configure nginx and SSL certificate (the domain name has not been filed, and the ssl certificate has not taken effect)
- `2.3` add Redis
- `2.4` added TS
- `2.5` supports PostgreSQL for image uploading
- `2.6` Front-end file separation (vue and ts), back-end implements permission management
- `2.7` Simple implementation of rights management
- `2.8` Adjust database structure && simple implementation of student course selection
- `2.9` Simple implementation of teacher-taught courses

> TODO: optimize the code

## start the service

1. Backend

   - go to the `backend` project
   - Find `main.py` right click to run (it is recommended to start with Pycharm)

   > Interface documentation: http://127.0.0.1:8000/docs

2. Front end

   - go to the `frontend` directory
   - `npm run dev` to run the project (Vscode is recommended)

   > Service interface: http://localhost:3000/

3. Effects

- login interface

  - `username`: `admin`

  - `password`: `123`

  - as shown

    ![](https://gitee.com/zxiaosi/image/raw/master/Project/Vue+FastAPI/frontend-login.png)

- Home (fake data)

  ![home](https://gitee.com/zxiaosi/image/raw/master/Project/Vue+FastAPI/home.png)

- `increment` of data

  ![add](https://gitee.com/zxiaosi/image/raw/master/Project/Vue+FastAPI/add.gif)

- `deletion` of data

  ![delete](https://gitee.com/zxiaosi/image/raw/master/Project/Vue+FastAPI/delete.gif)

- `change` of data

  ![update](https://gitee.com/zxiaosi/image/raw/master/Project/Vue+FastAPI/update.gif)

- search data

  ![](https://gitee.com/zxiaosi/image/raw/master/Project/Vue+FastAPI/search.gif)

- multi-select delete

  ![selectedDelete](https://gitee.com/zxiaosi/image/raw/master/Project/Vue+FastAPI/selectedDelete.gif)
