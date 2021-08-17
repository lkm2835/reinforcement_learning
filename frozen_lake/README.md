## Frozen Lake with RL

#### Default Setting

```
$ python3 main.py
```
![default_setting](./readme_image/default_setting.PNG)

#### User Setting 1 (==2)

```
 $ python3 main.py --learning_method 2 --episodes 3000 --discount_rate 0.5 --learning_rate 0.3 --slippery False
```

#### User Setting 2 (==1)

```
 $ python3 main.py -lm 2 -ep 3000 -dr 0.5 -lr 0.3 -sp N
```
![user_setting](./readme_image/user_setting.PNG)
<br><br>
---

#### Learning Method 1
![method1](./readme_image/method1.PNG)  
* use reward
<br>

#### Learning Method 2
![method2](./readme_image/method2.PNG)  
* use discounted reward
<br>

#### Learning Method 3
<img src="./readme_image/method3.PNG" width="700" height="70">  

* use discounted reward
* use learning rate

<br>
