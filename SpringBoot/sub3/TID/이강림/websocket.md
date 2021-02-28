# 채팅



## 1) websocket

- https://gnaseel.tistory.com/11 👌
  - Rest api에 소캣통신 구현

- https://blog.zvdev.com/2020/04/23/spring-socket-chat-room-example/
  - 소켓통신만으로 구현

- https://blog.naver.com/PostView.nhn?blogId=gomsun12&logNo=222068422927&categoryNo=29&parentCategoryNo=0&viewDate=&currentPage=1&postListTopCurrentPage=1&from=postView👌
  - 파일이 구조화가 잘 되어 있음
- https://hyeooona825.tistory.com/89 👌
  - @SendToUser : 1대1 으로 메세지를 보낼 때 사용하는 구조, /queue 경로를 일반적으로 사용
  - **intercepter** : Handshake 설정



```
: RestController의 경로를 통해 들어오면

TextWebSocketHandler 를 상속받은 클래스에서 Session을 저장하여
메세지가 들어올 경우, 저장된 Session들에게 메세지를 전달
```



## 2) stomp

- https://velog.io/@skyepodium/vue-spring-boot-stomp-%EC%9B%B9%EC%86%8C%EC%BC%93 : basic (알림 구현에 사용했던 오픈소스)

- https://asfirstalways.tistory.com/359 : 그닥 영양가 있지는 않음
- https://arincblossom.wordpress.com/2019/10/14/spring-boot-reactjs-websocket-%EC%B1%84%ED%8C%85-%EB%A7%8C%EB%93%A4%EA%B8%B0-1/ 👌 : Webconfig 설명이 매우 잘 되어 있음 : 1:1에 대한 가능성을 설명만 한다.. 아쉽다.. 밑에 부분을 조금더 자세히 읽어봐야할 것 같다..
  - SimpMessagingTemplate: 이 역시 클라이언트로 메시지를 보내는 방법 중 하나인데, 이 경우에는 convertAndSend에서 파라미터를 어떻게 설정하느냐에 따라 일대일, 즉 개인에게만 메시지를 전달 할 수 있다.
    혹은 convertAndSendToUser 메소드를 이용하여 파라미터에 사용자를 미리 지정할 수도 있다. 이 메소드를 사용하면 자동으로 user 형식으로 변경해준다.



```
1.@MessageMapping("/send") @SendTo("/subscribe") @Controller public class SocketController{...}
------------------------------------------------------------------------------
------------------------------------------------------------------------------

2. @Configuration @EnableWebSocketMessageBroker public class WebSocketConfig implements WebSocketMessageBrokerConfigurer{...}

------------------------------------------------------------------------------
2-1. configureMessageBroker

1) enableSimpleBroker("/subscribe") : subcribe 주소, subcribe 주소 -> this.stompClient.subscribe("/subscribe", ...)

2) setApplicationDestinationPrefixes("/prefix") : Front단의 send 접두어 -> this.stompClient.send("/prefix/send", JSON.stringify(msg), {});

3) setUserDestinationPrefix("/user") : 

------------------------------------------------------------------------------
2-2. registerStompEndpoints

1) setAllowedOrigins : CORS 해제 (다른식으로 해야함;)

2) addEndpoint("/connect") : connent 주소 = endpoint -> const serverURL = "http://localhost:8000/connect"

3) addInterceptors(new HttpHandshakeInterceptor()) : endpoint에 interceptor 추가하여 소캣 등록 
-> public class HttpHandshakeInterceptor implemet HandshakInterceptor {...} : connect를 할때, 3번 handshake 수행, get 방식 통신 / beforeHandshake : 3번의 handshake에 호출됨, http통신에 존재하는 SESSION 변수는 String 타입 / 	afterHandshake : handshake 후 호출됨


```





## 3) 장편

- https://blog.naver.com/PostView.nhn?blogId=scw0531&logNo=221052774287&parentCategoryNo=&categoryNo=&viewDate=&isShowPopularPosts=false&from=postView : 웹소켓

- https://blog.naver.com/PostView.nhn?blogId=scw0531&logNo=221097188275 : STOMP

```
그냥 위에서 나온 것들 반복...
```

<hr>



- https://basketdeveloper.tistory.com/78 : 백엔드(both) 👌 
  - **이벤트 리스너?** : WebSocket **연결/해제** 될 때 이벤트를 받아 **비즈니스 로직을 추가하거나 Log를 남기는 등의 작업**을 요할 때 **이벤트 리스너**를 설정
- https://ratseno.tistory.com/72?category=773803 : 프론트앤드(vanila html/css/js)

```
뭔가 답이 있는듯 한데.. 코틀린 같다.. 
```

- https://basketdeveloper.tistory.com/77?category=877627 : redis (그냥 진짜 redis에 대한 설명만 함, 현재는 패스)

<hr>



- https://daddyprogrammer.org/post/4077/spring-websocket-chatting/ : 6편 (1 소캣, 2 stomp, 3 redis, 4 jwt, 5 입퇴장 이벤트 처리, 6 WSS )

```
1편 : Websocket
1.하나의 채팅방 구현 
2.다수의 채팅방 구현 : 유저에 Session에 채팅방의 번호를 저장, 채팅방 별로 Session들을 묶어서 저장, message가 들어오면 해당하는 채팅방에 메세지 출력

2편 : Stomp
이것을 기준으로 구현 (보내는 주소를 나누는 것만 참고함)

```

- https://javaengine.tistory.com/ : 위에 꺼 배끼긴 헀는데, 그 외에 좋은 것도 많음 (설에 보면서 하기 좋을 수도..)

<hr>

<hr>



## 4) 고도화(redis)

https://dydtjr1128.github.io/spring/2019/05/26/Springboot-react-chatting.html : React (1)

https://handcoding.tistory.com/171 : js (2)

https://dzone.com/articles/build-a-chat-application-using-spring-boot-websock : 영어 (3)

