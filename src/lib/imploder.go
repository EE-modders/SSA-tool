package main

import (
	"bytes"
	"fmt"
	"./blast"
	"io/ioutil"
	"os"
)

func dcl_compressor(input []byte) {
	var b bytes.Buffer
	w := blast.NewWriter(&b, blast.Binary, blast.DictionarySize1024)
	w.Write(input)
	w.Close()
	os.Stdout.Write(b.Bytes())
	// fmt.Println(b.Bytes())
	// Output: [0 4 130 36 37 143 128 127]
}

func main(){
	// fmt.Println("Hello world!")
	// fmt.Println(os.Args[1])
	b, err := ioutil.ReadFile(os.Args[1])
	if err != nil {
		fmt.Print(err)
	}
	
	// fmt.Println(b)
	
	dcl_compressor(b)
}
