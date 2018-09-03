// Compile this file with: 
// clang -fobjc-arc objc.m

#import <Foundation/Foundation.h>

@interface SomeClass: NSObject
- (void)hello;
@end

@implementation SomeClass
- (void)hello {
  printf("Hello from SomeClass\n");
}
@end

int main() {
  SomeClass *obj = [SomeClass new];
  [obj hello];
  return 0;
}

