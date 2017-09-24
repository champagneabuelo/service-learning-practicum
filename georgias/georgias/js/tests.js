QUnit.test( "hello test", function( assert ) {
  assert.ok( 1 == "1", "Passed!" );
});

QUnit.test( "div visible", function ( assert) {
    var fixture = document.getElementById("qunit-fixture");
    addDonation(fixture);
    assert.equal(fixture.style.display, 'inline', "fixture is hidden");
});

QUnit.test( "div invisible", function ( assert) {
    var fixture = document.getElementById("qunit-fixture");
    fixture.style.display = 'inline';
    cancelDonation(fixture);
    assert.equal(fixture.style.display, 'none', "fixture is not hidden");
});
    
    