package 

import (
    "encoding/json"
    "errors"
)

const (
   UserNotFound int32 = 10000
   JobStatusMismatched int32 = 10001
   JobNotFound int32 = 10002
   SaveAlgoFailed int32 = 10003
   UpdateDbFailed int32 = 10004
   QueryDbFailed int32 = 10005
   testError int32 = 10006
   bbb int32 = 10007
   aaa int32 = 10008
)

var ErrMsg = map[int32]string {
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
    Code int32    `json:"code"`
    Msg string    `json:"msg"`
	Detail string `json:"detail"`
}

func (ce *Error)Error()(error) {
    return errors.New(string(ce.Json()))
}

func (ce *Error)Json()([]byte) {
    s, _ := json.Marshal(ce)
    return s
}

func (ce *Error)String() string {
	return string(ce.Json())
}

func GenSuccess() *Error {
	return GenError(Success)
}

func FromJson(buf []byte)(*Error, error) {
    var ce Error
    err := json.Unmarshal(buf, &ce)
    if err != nil {
        return nil, err
    }
    return &ce, nil
}

// func GenJson(errCode int32) ([]byte) {
//     return (&Error{errCode, ErrMsg[errCode], ErrMsg[errCode]}).Json()
// }

func GenError(errCode int32) (*Error) {
	return &Error{errCode, ErrMsg[errCode], ""}
}

func GenErrorWithInfo(errCode int32, info string) (*Error) {
	return &Error{errCode, ErrMsg[errCode], info}
}
