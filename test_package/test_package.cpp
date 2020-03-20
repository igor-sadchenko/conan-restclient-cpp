#include <iostream>
#include <restclient-cpp/restclient.h>


#define EXPECT_TRUE(arg) \
        do { \
            if(!(arg)) { \
                std::cerr << "Unexpected false at " \
                        << __FILE__ << ", " << __LINE__ << ", " << __func__ << ": " << #arg << ": \033[31mFAILED\033[0m\n"; \
                return -1; } \
            else { \
                std::cout << __FILE__ << ", " << __LINE__ << ", " << __func__ << ": \033[32mPASSED\033[0m\n"; } \
        } while(false);

// This is a simple example
int main()
{
    // DELETE
    RestClient::Response del = RestClient::del("http://httpbin.org/delete");
    EXPECT_TRUE(200 == del.code);

    // Non exist site
    std::string u = "http://nonexistent";
    del = RestClient::del(u);
    EXPECT_TRUE(-1 == del.code);

    // GET
    RestClient::Response get = RestClient::get("http://httpbin.org");
    EXPECT_TRUE(200 == get.code);

    // POST
    RestClient::Response post = RestClient::post("http://httpbin.org/post", "text/json", "{\"foo\": \"bla\"}");
     EXPECT_TRUE(200 == post.code);

    // PUT
    RestClient::Response put = RestClient::put("http://httpbin.org/put", "text/json", "{\"foo\": \"bla\"}");
    EXPECT_TRUE(200 == put.code);

    // HEAD
    RestClient::Response head = RestClient::head("http://httpbin.org/");
    EXPECT_TRUE(200 == head.code);

    return 0;
}