package main

/*
	패키지 Scope
	- 패키지 내에 있는 객체들의 이름이 첫 문자가 ' 대 '문자일 경우 : public 으로 사용 됨
	- 패키지 내에 있는 객체들의 이름이 첫 문자가 ' 소 '문자일 경우 : non - public 으로 패키지 내부에서만 사용 됨
	패키지 alias
	- import 시 패키지에 이름을 붙여 줌
	import smpl "testlib"
	import [alias 명]	"패키지 명"
*/
import (
	"fmt"
	//testpkg "test/testlib"
)

// main 함수는 폴더당 하나씩 존재 할 수 있음 > 확인이 좀 더 필요함
func main() {

	//song := testpkg.GetMusic("Alicia Keys")
	//println(song)

	fmt.Println("hello, world")
	fmt.Println("안녕, 세상")

	// 조건문 while 예제
	// var a = 2 와 같은 의미 'Short Assignment Statement ( := )'
	a := 2
	fmt.Println("check 함수 입력 값 : ", a)
	check(2)

	// 함수 예제
	msg := "Hello"

	say1(msg)

	// go lang에서는 포인터 사용 가능
	// 단, C언어에서 하는 포인터 연산은 불가능 (포인터 단순 기능)
	say2(&msg)
	println(msg)

	total1 := sum1(1, 7, 3, 5, 9, 10)
	println(total1)

	count, total2 := sum2(1, 7, 3, 5, 9)
	println(count, total2)

	f := calc() // calc 함수를 실행하여 리턴값으로 나온 클로저를 변수에 저장

	fmt.Println(f(1)) // 8
	// ⅱ 참고사항.
	// fmt.Println(f.ab) 형태로 변수에 직접적인 접근이 불가. (∴지역변수는 소멸했기 떄문)
	// f2(1) 과 같이 ab, ab에 대한 변수 값에 대해 재 사용이 가능 함이 중요 ★
	f2 := calc() // calc 함수를 실행하여 리턴값으로 나온 클로저를 변수에 저장

	fmt.Println("클로저 함수 : ", f2(1))
	fmt.Println("클로저 함수 : ", f2(2))

	// 슬라이스 ≒ 동적할당
	// var sli []int        // 슬라이스 변수 선언
	sli := []int{0, 1, 2, 3, 4, 5} // 슬라이스에 리터럴값 지정
	sli = sli[2:6]                 // 슬라이스 [2]번 인덱스 ~ [5]번 인덱스 까지 저장
	sli = sli[1:]                  // 슬라이스 [1]번 인덱스 부터 마지막 인덱스 까지 저장
	sli[1] = 10                    // 슬라이스 [1]번 인덱스 값 '10'으로 변경 함
	fmt.Println("a : ", sli)

	s := make([]int, 5, 10)
	println(len(s), cap(s)) //len 5, cap 10

	// 슬라이스에 별도 길이와 용량 미지정 시 기본적으로 길이와 용량이 0인 슬라이스를 만듦 >> Nil Slice
	var NSli []int
	if NSli == nil {
		println("Nil Slice")
	}
	println(len(NSli), cap(NSli)) // 모두 0

	// 슬라이스 추가
	sliAdd := []int{0, 1}
	fmt.Println(sliAdd) // [0 1] 출력
	sliAdd = append(sliAdd, 2)
	fmt.Println(sliAdd) // [0 1 2] 출력
	sliAdd = append(sliAdd, 3, 4, 5)
	fmt.Println(sliAdd) // [0 1 3 4 5] 출력

	// 슬라이스 복사
	sliceA := []int{1, 2, 3}
	sliceB := []int{4, 5, 6}

	sliceA = append(sliceA, sliceB...)
	//sliceA = append(sliceA, 4, 5, 6) 같은 의미로 생각하면 됨
	fmt.Println(sliceA)

	appendA := make([]int, 3, 4) // len: 3 cap: 4인 slice 생성
	appendA[0] = 10
	appendA[1] = 20
	appendA[2] = 30

	appendB := append(appendA, 40) // appendA에 여분의 용량이 남으므로 내부배열 공유
	appendC := append(appendA, 50) // appendA에 여분의 용량이 남으므로 내부배열 공유
	appendD := append(appendC, 60) // appendC에 여분의 용량이 남지 않으므로 새로운 내부배열 할당

	fmt.Println(appendA, len(appendA), cap(appendA)) // [10 20 30] 3 4
	fmt.Println(appendB, len(appendB), cap(appendB)) // [10 20 30 50] 4 4
	fmt.Println(appendC, len(appendC), cap(appendC)) // [10 20 30 50] 4 4
	fmt.Println(appendD, len(appendD), cap(appendD)) // [10 20 30 50 60] 5 8

	//Go에서 "go" 키워드를 사용하여 함수를 호출하면, 런타임시 새로운 goroutine을 실행한다.

	// for 문 (조건식 만 사용)
	forRnum := 1
	for forRnum < 100 {
		forRnum *= 2
	}
	println("for 문 조건식 만 사용 : ", forRnum)

	// for range 문
	names := []string{"홍길동", "이순신", "강감찬"}

	for index, name := range names {
		println(index, name)
	}

	// break, continue, goto문
	var breakA = 1
	for breakA < 15 {
		if breakA == 5 {
			breakA += breakA
			continue // for 루프 시작으로 감
		}
		breakA++
		if breakA > 10 {
			break // 루프 이탈
		}
	}
	if breakA == 11 {
		goto END // goto 사용예
	}
	println(a)

END:
	println("for문 break, continue, goto문 예제 종료")

	// Go 채널 - make() 함수를 통해 미리 생성 되어야 하며, 채널 연산자 '<-'을 통해 데이터를 송수신 함.
	// 채널은 흔히 Goroutine들 사이 데이터를 주고 받는데 사용 됨.
	// 상대편이 준비될 때까지 채널에서 대기하며, 데이터를 동기화하는데 사용 됨
	// 정수형 채널 생성 > goroutine 에서 그 채널에 123이란 정수데이터를 송신 > 메인 루틴에서 채널로부터 123데이터를 수신 하는 예제

	//정수형 채널 생성
	ch := make(chan int)

	go func() {
		ch <- 123 // 채널에 123을 송신
	}()

	var i int
	i = <-ch //채널로부터 123을 수신
	println("Go 채널 예제 : ", i)

	// Go 채널 예제 1) Unbuffered Channel : 하나의 수신자가 데이타를 받을 때까지 송신자가 데이터를 보내는 채널에 대기
	done := make(chan bool)
	go func() {
		for eNum := 0; eNum < 10; eNum++ {
			fmt.Println(eNum)
		}
		done <- true
	}()

	// 위의 Go루틴이 끝날때까지 대기
	<-done

	// Go 채널 예제 2) Buffered Channel : 
}

func calc() func(x int) int {
	ab, ba := 3, 5 // 지역 변수는 함수가 끝나면 소멸되지만
	return func(x int) int {
		return ab*x + ba // 클로저이므로 함수를 호출 할 때마다 변수 a와 b의 값을 사용할 수 있음
		// 참고사항 -> ⅱ
	}
	// ↑ 익명 함수를 리턴
}

// sum1 함수를 sum2 함수로 정리 할 수 있음
// 가변인자함수 는 ' ... ' 로 표시함 3개 고정.
func sum1(nums ...int) int {
	s := 0
	for _, n := range nums {
		s += n
	}
	return s
}

func sum2(nums ...int) (count int, total int) {
	for _, n := range nums {
		total += n
	}
	count = len(nums)
	return
}

func say1(msg string) {
	println("Pass By Value : " + msg)
}

func say2(msg *string) {
	println("Pass By Reference : " + *msg)
	// 메시지 변경
	*msg = "Changed"
}

// Switch 문
func check(val int) {

	switch val {
	/*
		// ⅰ ) 변수 v의 타입 체크 후 case 블럭 실행
		switch v.(type) {
			case int:
			println("int")
			...}

		// ⅱ ) Expression을 사용한 경우
		switch x := category << 2; x - 1 {
			...}

		// ⅲ ) Expression을 적지 않는 용법
		switch {
			case score >= 90:
				println("A")
			case score >= 80:
				println("B")
			case score >= 70:
				println("C")
			case score >= 60:
				println("D")
			default:
				println("No Hope")
		}
	*/

	// case int:
	case 1:
		fmt.Println("1 이하")
		// go lang 에서는 break 문을 명시 하지 않아도 자동 break 해줌.
		// 따라서 case 1: 실행 후 case 2: 실행을 원할 때
		// ' fallthrough ' 문을 사용 하여 계속 연산하게 해줌
	case 2:
		fmt.Println("2 이하")
		fallthrough

	case 3:
		fmt.Println("3 이하")
	}
}

/*
추가 내용
구조체, 메서드, 인터페이스, 예외처리, defer, panic, GO 루틴

// defer 예제 - 파일을 Open 한 후 바로 파일을 Close하는 작업을 defer로 쓰고 있다.
이는 차후 문장에서 어떤 에러가 발생하더라도 항상 파일을 Close할 수 있도록 한다.
func main() {
    f, err := os.Open("1.txt")
    if err != nil {
        panic(err)
    }

    // main 마지막에 파일 close 실행
    defer f.Close()

    // 파일 읽기
    bytes := make([]byte, 1024)
    f.Read(bytes)
    println(len(bytes))
}

// panic 예제 - 현재 함수를 즉시 멈추고 현재 함수에 defer 함수들을 모두 실행한 후 즉시 리턴한다.
이러한 panic 모드 실행 방식은 다시 상위함수에도 똑같이 적용되고, 계속 콜스택을 타고 올라가며 적용된다.
그리고 마지막에는 프로그램이 에러를 내고 종료하게 된다.
func main() {
    openFile("Invalid.txt")
    println("Done") //이 문장은 실행 안됨
}

func openFile(fn string) {
    f, err := os.Open(fn)
    if err != nil {
        panic(err)
    }
    // 파일 close 실행됨
    defer f.Close()
}

//recover - panic 함수에 의한 패닉상태를 다시 정상상태로 되돌리는 함수이다.
(위의 panic 예제에서는 main 함수에서 println() 이 호출되지 못하고 프로그램이 crash 하지만, 아래와 예제와 같이 recover 함수를 사용하면 panic 상태를 제거하고 openFile()의 다음 문장인 println() 을 호출하게 된다.)
func main() {
    openFile("1.txt")
    println("Done") // 이 문장 실행됨
}

func openFile(fn string) {
    // defere 함수. panic 호출시 실행됨
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("OPEN ERROR", r)
        }
    }()

    f, err := os.Open(fn)
    if err != nil {
        panic(err)
    }

    // 파일 close 실행됨
    defer f.Close()
}
*/
