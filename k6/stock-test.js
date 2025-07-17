import http from 'k6/http';
import { check } from 'k6';

export default function () {
  let res = http.get('http://localhost:8080/api/stock/some_endpoint');
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
}
