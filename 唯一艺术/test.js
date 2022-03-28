const crypto = require('crypto-js')

function get_encrypt(t, a) {
    var e = "4tBlCLWFZ3eD93CvDE2lpw=="
    var s = crypto.enc.Base64.parse(e)
      , r = JSON.stringify({
        id: t.substr(0, t.length - 1),
        sum: a
    })
      , i = crypto.enc.Utf8.parse(r)
      , _ = crypto.AES.encrypt(i, s, {
        mode: crypto.mode.ECB,
        padding: crypto.pad.Pkcs7
    });
    return _.toString()
};

function get_decrypt(e) {
    var d = "5opkytHOggKj5utjZOgszg=="
    var t = crypto.enc.Base64.parse(d)
      , a =crypto.AES.decrypt(e, t, {
        mode: crypto.mode.ECB,
        padding: crypto.pad.Pkcs7
    });
    return crypto.enc.Utf8.stringify(a).toString()
}
e = "truiLeKm7AKyuie+33QCYQbQbIFV/sMRZWJmwqeNgkXAsI/btPSFu46HvCNTdR9oYvYQbko8JRK37s99LQjCI5AFMHngY6I9MLDmSgQ4F6dhW2UCotDRo0gDayBnXNKzJhkZTK0QxlinmU60CGhpP5v4vBbq5xqmNiMwiJ1FCP0pPuFT7ud1Ajia3NtUxnwLMnwODiKmE9SJMHjnvQwC9w=="
// console.log(get_decrypt(e))
console.log(get_encrypt("ee758dc2dd5812e187c64ee97c2bf5a2}", "395428"))

module.exports = {
    get_encrypt,
    get_decrypt,
}
