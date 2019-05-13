package ${package_name}

import (
    "encoding/json"
    "errors"
)

type ErrCode int

const (
% for err_info in err_infos:
   ${err_info.code} ErrCode = ${err_info.number}
% endfor
)

var ErrMsgMap = map[ErrCode]string {
% for err_info in err_infos:
    ${err_info.code}:"${err_info.msg}",
% endfor
}

type CustomError struct {
    ErrCode ErrCode  `json:"err_code"`
    ErrMsg string    `json:"err_msg"`
}

func (ce *CustomError)ToError()(error) {
    bError, _ := json.Marshal(ce)
    return errors.New(string(bError))
}

func GenError(errCode ErrCode) (err error) {
    bError, _ := json.Marshal(CustomError{errCode, ErrMsgMap[errCode]})
    return errors.New(string(bError))
}

func WithInfoError(errCode ErrCode ,info string) (err error) {
    bError, _ := json.Marshal(CustomError{errCode, ErrMsgMap[errCode] + ":" + info})
    return errors.New(string(bError))
}
