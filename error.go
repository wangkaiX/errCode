package errno

import (
    "fmt"
    "encoding/json"
    "errors"
)

type ErrCode int

const (
   UserNotFound ErrCode = 40000
   JobStatusMismatched ErrCode = 40001
   JobNotFound ErrCode = 40002
   SaveAlgoFailed ErrCode = 40003
   UpdateDbFailed ErrCode = 40004
   QueryDbFailed ErrCode = 40005
   testError ErrCode = 40006
   bbb ErrCode = 40007
   aaa ErrCode = 40008
)

var ErrMsg = map[ErrCode]string {
    UserNotFound:"用户不存在",
    JobStatusMismatched:"作业状态不匹配",
    JobNotFound:"作业不存在",
    SaveAlgoFailed:"保存算法失败",
    UpdateDbFailed:"更新数据库失败",
    QueryDbFailed:"查询数据库失败",
    testError:"测试错误码",
    bbb:"bbb",
    aaa:"aaa",
}

type Error struct {
    ErrCode ErrCode  `json:"err_code"`
    ErrMsg string    `json:"err_msg"`
}

func (ce *Error)ToError()(error) {
    return errors.New(string(ce.ToJson()))
}

func (ce *Error)ToJson()([]byte) {
    s, _ := json.Marshal(ce)
    return s
}

func FromJson(buf []byte)(*Error, error) {
    var ce Error
    err := json.Unmarshal(buf, &ce)
    if err != nil {
        return nil, err
    }
    return &ce, nil
}

func GenJson(errCode ErrCode) ([]byte) {
    return (&Error{errCode, ErrMsg[errCode]}).ToJson()
}

func GenError(errCode ErrCode) (err error) {
    bError, _ := json.Marshal(Error{errCode, ErrMsg[errCode]})
    return errors.New(string(bError))
}

func WithInfoError(errCode ErrCode ,info string) (err error) {
    bError, _ := json.Marshal(Error{errCode, fmt.Sprintf("%s[%s]", ErrMsg[errCode], info)})
    return errors.New(string(bError))
}
