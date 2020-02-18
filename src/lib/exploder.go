package main

import (
	"./blast"
	"io"
	"os"
)

func dcl_decompressor(a io.Reader) {
	r, err := blast.NewReader(a)
	if err != nil {
		panic(err)
	}
	io.Copy(os.Stdout, r)
	r.Close()
}

func main(){
	// fmt.Println("Blast: PKWare Data Compression Library (DCL) written in Go")
	// fmt.Println("original code can be found: https://github.com/JoshVarga/blast")
	// fmt.Println("all credits go to him, thank you for allowing me to use this sourcecode!!")
	
	file, err := os.Open(os.Args[1])
	if err != nil {
		panic(err)
	}	
	dcl_decompressor(file)
}
