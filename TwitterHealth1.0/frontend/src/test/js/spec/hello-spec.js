// hello.js
// --- dummy test for checking the installation of jsTestDriver and jasmine

require([], function () {
    
    describe("HelloWorldTest", function () {
        it("should return hello world!", function () {
            expect("hello world!").toEqual("hello world!");
        });
    });
    
});