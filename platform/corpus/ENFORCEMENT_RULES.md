# Enforcements and Rules

<!-- atom:begin id=ENF-0001 -->
```yaml
id: ENF-0001
type: enforcement
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Block merge"
tags: [ladder]
on_fail: block-merge
```
<!-- atom:end id=ENF-0001 -->

<!-- atom:begin id=ENF-0002 -->
```yaml
id: ENF-0002
type: enforcement
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Refuse spawn"
tags: [ladder]
on_fail: refuse-spawn
```
<!-- atom:end id=ENF-0002 -->

<!-- atom:begin id=ENF-0003 -->
```yaml
id: ENF-0003
type: enforcement
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Suspend and escalate"
tags: [ladder]
on_fail: suspend-escalate
escalation_target: tribune-veto-queue
```
<!-- atom:end id=ENF-0003 -->

<!-- atom:begin id=ENF-0004 -->
```yaml
id: ENF-0004
type: enforcement
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Advisory"
tags: [ladder]
on_fail: advisory
```
<!-- atom:end id=ENF-0004 -->

<!-- atom:begin id=RULE-0001 -->
```yaml
id: RULE-0001
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0002 via CTRL-0001"
tags: [binding]
claim: SPEC-0002
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0002 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0001 -->

<!-- atom:begin id=RULE-0002 -->
```yaml
id: RULE-0002
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0004 via CTRL-0001"
tags: [binding]
claim: SPEC-0004
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0004 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0002 -->

<!-- atom:begin id=RULE-0003 -->
```yaml
id: RULE-0003
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0005 via CTRL-0001"
tags: [binding]
claim: SPEC-0005
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0005 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0003 -->

<!-- atom:begin id=RULE-0004 -->
```yaml
id: RULE-0004
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0006 via CTRL-0001"
tags: [binding]
claim: SPEC-0006
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0006 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0004 -->

<!-- atom:begin id=RULE-0005 -->
```yaml
id: RULE-0005
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0007 via CTRL-0001"
tags: [binding]
claim: SPEC-0007
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0007 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0005 -->

<!-- atom:begin id=RULE-0006 -->
```yaml
id: RULE-0006
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0008 via CTRL-0001"
tags: [binding]
claim: SPEC-0008
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0008 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0006 -->

<!-- atom:begin id=RULE-0007 -->
```yaml
id: RULE-0007
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0009 via CTRL-0008"
tags: [binding]
claim: SPEC-0009
control: CTRL-0008
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0009 }
  - { rel: binds, target: CTRL-0008 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0007 -->

<!-- atom:begin id=RULE-0008 -->
```yaml
id: RULE-0008
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind RSTR-0001 via CTRL-0001"
tags: [binding]
claim: RSTR-0001
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: RSTR-0001 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0008 -->

<!-- atom:begin id=RULE-0009 -->
```yaml
id: RULE-0009
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0011 via CTRL-0001"
tags: [binding]
claim: SPEC-0011
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0011 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0009 -->

<!-- atom:begin id=RULE-0010 -->
```yaml
id: RULE-0010
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0012 via CTRL-0008"
tags: [binding]
claim: SPEC-0012
control: CTRL-0008
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0012 }
  - { rel: binds, target: CTRL-0008 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0010 -->

<!-- atom:begin id=RULE-0011 -->
```yaml
id: RULE-0011
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0013 via CTRL-0001"
tags: [binding]
claim: SPEC-0013
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0013 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0011 -->

<!-- atom:begin id=RULE-0012 -->
```yaml
id: RULE-0012
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0014 via CTRL-0001"
tags: [binding]
claim: SPEC-0014
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0014 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0012 -->

<!-- atom:begin id=RULE-0013 -->
```yaml
id: RULE-0013
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0015 via CTRL-0001"
tags: [binding]
claim: SPEC-0015
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0015 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0013 -->

<!-- atom:begin id=RULE-0014 -->
```yaml
id: RULE-0014
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0016 via CTRL-0001"
tags: [binding]
claim: SPEC-0016
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0016 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0014 -->

<!-- atom:begin id=RULE-0015 -->
```yaml
id: RULE-0015
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0017 via CTRL-0003"
tags: [binding]
claim: SPEC-0017
control: CTRL-0003
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0017 }
  - { rel: binds, target: CTRL-0003 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0015 -->

<!-- atom:begin id=RULE-0016 -->
```yaml
id: RULE-0016
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind RSTR-0003 via CTRL-0001"
tags: [binding]
claim: RSTR-0003
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: RSTR-0003 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0016 -->

<!-- atom:begin id=RULE-0017 -->
```yaml
id: RULE-0017
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0018 via CTRL-0006"
tags: [binding]
claim: SPEC-0018
control: CTRL-0006
enforcement: ENF-0002
relations:
  - { rel: binds, target: SPEC-0018 }
  - { rel: binds, target: CTRL-0006 }
  - { rel: binds, target: ENF-0002 }
```
<!-- atom:end id=RULE-0017 -->

<!-- atom:begin id=RULE-0018 -->
```yaml
id: RULE-0018
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0019 via CTRL-0005"
tags: [binding]
claim: SPEC-0019
control: CTRL-0005
enforcement: ENF-0002
relations:
  - { rel: binds, target: SPEC-0019 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0002 }
```
<!-- atom:end id=RULE-0018 -->

<!-- atom:begin id=RULE-0019 -->
```yaml
id: RULE-0019
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0020 via CTRL-0001"
tags: [binding]
claim: SPEC-0020
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0020 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0019 -->

<!-- atom:begin id=RULE-0020 -->
```yaml
id: RULE-0020
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0021 via CTRL-0001"
tags: [binding]
claim: SPEC-0021
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0021 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0020 -->

<!-- atom:begin id=RULE-0021 -->
```yaml
id: RULE-0021
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0022 via CTRL-0001"
tags: [binding]
claim: SPEC-0022
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0022 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0021 -->

<!-- atom:begin id=RULE-0022 -->
```yaml
id: RULE-0022
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0023 via CTRL-0008"
tags: [binding]
claim: SPEC-0023
control: CTRL-0008
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0023 }
  - { rel: binds, target: CTRL-0008 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0022 -->

<!-- atom:begin id=RULE-0023 -->
```yaml
id: RULE-0023
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0024 via CTRL-0001"
tags: [binding]
claim: SPEC-0024
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0024 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0023 -->

<!-- atom:begin id=RULE-0024 -->
```yaml
id: RULE-0024
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0025 via CTRL-0008"
tags: [binding]
claim: SPEC-0025
control: CTRL-0008
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0025 }
  - { rel: binds, target: CTRL-0008 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0024 -->

<!-- atom:begin id=RULE-0025 -->
```yaml
id: RULE-0025
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0026 via CTRL-0001"
tags: [binding]
claim: SPEC-0026
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0026 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0025 -->

<!-- atom:begin id=RULE-0026 -->
```yaml
id: RULE-0026
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0027 via CTRL-0001"
tags: [binding]
claim: SPEC-0027
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0027 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0026 -->

<!-- atom:begin id=RULE-0027 -->
```yaml
id: RULE-0027
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0028 via CTRL-0001"
tags: [binding]
claim: SPEC-0028
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0028 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0027 -->

<!-- atom:begin id=RULE-0028 -->
```yaml
id: RULE-0028
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind RSTR-0005 via CTRL-0002"
tags: [binding]
claim: RSTR-0005
control: CTRL-0002
enforcement: ENF-0001
relations:
  - { rel: binds, target: RSTR-0005 }
  - { rel: binds, target: CTRL-0002 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0028 -->

<!-- atom:begin id=RULE-0029 -->
```yaml
id: RULE-0029
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0029 via CTRL-0001"
tags: [binding]
claim: SPEC-0029
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0029 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0029 -->

<!-- atom:begin id=RULE-0030 -->
```yaml
id: RULE-0030
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0030 via CTRL-0003"
tags: [binding]
claim: SPEC-0030
control: CTRL-0003
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0030 }
  - { rel: binds, target: CTRL-0003 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0030 -->

<!-- atom:begin id=RULE-0031 -->
```yaml
id: RULE-0031
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0031 via CTRL-0003"
tags: [binding]
claim: SPEC-0031
control: CTRL-0003
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0031 }
  - { rel: binds, target: CTRL-0003 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0031 -->

<!-- atom:begin id=RULE-0032 -->
```yaml
id: RULE-0032
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0033 via CTRL-0001"
tags: [binding]
claim: SPEC-0033
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0033 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0032 -->

<!-- atom:begin id=RULE-0033 -->
```yaml
id: RULE-0033
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0034 via CTRL-0001"
tags: [binding]
claim: SPEC-0034
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0034 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0033 -->

<!-- atom:begin id=RULE-0034 -->
```yaml
id: RULE-0034
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0035 via CTRL-0001"
tags: [binding]
claim: SPEC-0035
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0035 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0034 -->

<!-- atom:begin id=RULE-0035 -->
```yaml
id: RULE-0035
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0036 via CTRL-0001"
tags: [binding]
claim: SPEC-0036
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0036 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0035 -->

<!-- atom:begin id=RULE-0036 -->
```yaml
id: RULE-0036
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0037 via CTRL-0008"
tags: [binding]
claim: SPEC-0037
control: CTRL-0008
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0037 }
  - { rel: binds, target: CTRL-0008 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0036 -->

<!-- atom:begin id=RULE-0037 -->
```yaml
id: RULE-0037
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0038 via CTRL-0007"
tags: [binding]
claim: SPEC-0038
control: CTRL-0007
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0038 }
  - { rel: binds, target: CTRL-0007 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0037 -->

<!-- atom:begin id=RULE-0038 -->
```yaml
id: RULE-0038
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind RSTR-0006 via CTRL-0001"
tags: [binding]
claim: RSTR-0006
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: RSTR-0006 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0038 -->

<!-- atom:begin id=RULE-0039 -->
```yaml
id: RULE-0039
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0039 via CTRL-0007"
tags: [binding]
claim: SPEC-0039
control: CTRL-0007
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0039 }
  - { rel: binds, target: CTRL-0007 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0039 -->

<!-- atom:begin id=RULE-0040 -->
```yaml
id: RULE-0040
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0040 via CTRL-0007"
tags: [binding]
claim: SPEC-0040
control: CTRL-0007
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0040 }
  - { rel: binds, target: CTRL-0007 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0040 -->

<!-- atom:begin id=RULE-0041 -->
```yaml
id: RULE-0041
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0041 via CTRL-0008"
tags: [binding]
claim: SPEC-0041
control: CTRL-0008
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0041 }
  - { rel: binds, target: CTRL-0008 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0041 -->

<!-- atom:begin id=RULE-0042 -->
```yaml
id: RULE-0042
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0043 via CTRL-0006"
tags: [binding]
claim: SPEC-0043
control: CTRL-0006
enforcement: ENF-0002
relations:
  - { rel: binds, target: SPEC-0043 }
  - { rel: binds, target: CTRL-0006 }
  - { rel: binds, target: ENF-0002 }
```
<!-- atom:end id=RULE-0042 -->

<!-- atom:begin id=RULE-0043 -->
```yaml
id: RULE-0043
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind RSTR-0007 via CTRL-0002"
tags: [binding]
claim: RSTR-0007
control: CTRL-0002
enforcement: ENF-0001
relations:
  - { rel: binds, target: RSTR-0007 }
  - { rel: binds, target: CTRL-0002 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0043 -->

<!-- atom:begin id=RULE-0044 -->
```yaml
id: RULE-0044
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind RSTR-0008 via CTRL-0006"
tags: [binding]
claim: RSTR-0008
control: CTRL-0006
enforcement: ENF-0002
relations:
  - { rel: binds, target: RSTR-0008 }
  - { rel: binds, target: CTRL-0006 }
  - { rel: binds, target: ENF-0002 }
```
<!-- atom:end id=RULE-0044 -->

<!-- atom:begin id=RULE-0045 -->
```yaml
id: RULE-0045
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0044 via CTRL-0006"
tags: [binding]
claim: SPEC-0044
control: CTRL-0006
enforcement: ENF-0002
relations:
  - { rel: binds, target: SPEC-0044 }
  - { rel: binds, target: CTRL-0006 }
  - { rel: binds, target: ENF-0002 }
```
<!-- atom:end id=RULE-0045 -->

<!-- atom:begin id=RULE-0046 -->
```yaml
id: RULE-0046
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0045 via CTRL-0001"
tags: [binding]
claim: SPEC-0045
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0045 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0046 -->

<!-- atom:begin id=RULE-0047 -->
```yaml
id: RULE-0047
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0046 via CTRL-0004"
tags: [binding]
claim: SPEC-0046
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0046 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0047 -->

<!-- atom:begin id=RULE-0048 -->
```yaml
id: RULE-0048
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0047 via CTRL-0003"
tags: [binding]
claim: SPEC-0047
control: CTRL-0003
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0047 }
  - { rel: binds, target: CTRL-0003 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0048 -->

<!-- atom:begin id=RULE-0049 -->
```yaml
id: RULE-0049
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0048 via CTRL-0004"
tags: [binding]
claim: SPEC-0048
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0048 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0049 -->

<!-- atom:begin id=RULE-0050 -->
```yaml
id: RULE-0050
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0049 via CTRL-0001"
tags: [binding]
claim: SPEC-0049
control: CTRL-0001
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0049 }
  - { rel: binds, target: CTRL-0001 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0050 -->

<!-- atom:begin id=RULE-0051 -->
```yaml
id: RULE-0051
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind RSTR-0010 via CTRL-0004"
tags: [binding]
claim: RSTR-0010
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: RSTR-0010 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0051 -->

<!-- atom:begin id=RULE-0052 -->
```yaml
id: RULE-0052
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind RSTR-0011 via CTRL-0004"
tags: [binding]
claim: RSTR-0011
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: RSTR-0011 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0052 -->

<!-- atom:begin id=RULE-0053 -->
```yaml
id: RULE-0053
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0050 via CTRL-0004"
tags: [binding]
claim: SPEC-0050
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0050 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0053 -->

<!-- atom:begin id=RULE-0054 -->
```yaml
id: RULE-0054
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0051 via CTRL-0004"
tags: [binding]
claim: SPEC-0051
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0051 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0054 -->

<!-- atom:begin id=RULE-0055 -->
```yaml
id: RULE-0055
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0052 via CTRL-0004"
tags: [binding]
claim: SPEC-0052
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0052 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0055 -->

<!-- atom:begin id=RULE-0056 -->
```yaml
id: RULE-0056
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0053 via CTRL-0008"
tags: [binding]
claim: SPEC-0053
control: CTRL-0008
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0053 }
  - { rel: binds, target: CTRL-0008 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0056 -->

<!-- atom:begin id=RULE-0057 -->
```yaml
id: RULE-0057
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0054 via CTRL-0005"
tags: [binding]
claim: SPEC-0054
control: CTRL-0005
enforcement: ENF-0002
relations:
  - { rel: binds, target: SPEC-0054 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0002 }
```
<!-- atom:end id=RULE-0057 -->

<!-- atom:begin id=RULE-0058 -->
```yaml
id: RULE-0058
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0055 via CTRL-0006"
tags: [binding]
claim: SPEC-0055
control: CTRL-0006
enforcement: ENF-0002
relations:
  - { rel: binds, target: SPEC-0055 }
  - { rel: binds, target: CTRL-0006 }
  - { rel: binds, target: ENF-0002 }
```
<!-- atom:end id=RULE-0058 -->

<!-- atom:begin id=RULE-0059 -->
```yaml
id: RULE-0059
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0056 via CTRL-0002"
tags: [binding]
claim: SPEC-0056
control: CTRL-0002
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0056 }
  - { rel: binds, target: CTRL-0002 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0059 -->

<!-- atom:begin id=RULE-0060 -->
```yaml
id: RULE-0060
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0057 via CTRL-0008"
tags: [binding]
claim: SPEC-0057
control: CTRL-0008
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0057 }
  - { rel: binds, target: CTRL-0008 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0060 -->

<!-- atom:begin id=RULE-0061 -->
```yaml
id: RULE-0061
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0058 via CTRL-0004"
tags: [binding]
claim: SPEC-0058
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0058 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0061 -->

<!-- atom:begin id=RULE-0062 -->
```yaml
id: RULE-0062
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind RSTR-0013 via CTRL-0006"
tags: [binding]
claim: RSTR-0013
control: CTRL-0006
enforcement: ENF-0002
relations:
  - { rel: binds, target: RSTR-0013 }
  - { rel: binds, target: CTRL-0006 }
  - { rel: binds, target: ENF-0002 }
```
<!-- atom:end id=RULE-0062 -->

<!-- atom:begin id=RULE-0063 -->
```yaml
id: RULE-0063
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0059 via CTRL-0006"
tags: [binding]
claim: SPEC-0059
control: CTRL-0006
enforcement: ENF-0002
relations:
  - { rel: binds, target: SPEC-0059 }
  - { rel: binds, target: CTRL-0006 }
  - { rel: binds, target: ENF-0002 }
```
<!-- atom:end id=RULE-0063 -->

<!-- atom:begin id=RULE-0064 -->
```yaml
id: RULE-0064
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0060 via CTRL-0006"
tags: [binding]
claim: SPEC-0060
control: CTRL-0006
enforcement: ENF-0002
relations:
  - { rel: binds, target: SPEC-0060 }
  - { rel: binds, target: CTRL-0006 }
  - { rel: binds, target: ENF-0002 }
```
<!-- atom:end id=RULE-0064 -->

<!-- atom:begin id=RULE-0065 -->
```yaml
id: RULE-0065
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0061 via CTRL-0002"
tags: [binding]
claim: SPEC-0061
control: CTRL-0002
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0061 }
  - { rel: binds, target: CTRL-0002 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0065 -->

<!-- atom:begin id=RULE-0066 -->
```yaml
id: RULE-0066
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind RSTR-0014 via CTRL-0005"
tags: [binding]
claim: RSTR-0014
control: CTRL-0005
enforcement: ENF-0002
relations:
  - { rel: binds, target: RSTR-0014 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0002 }
```
<!-- atom:end id=RULE-0066 -->

<!-- atom:begin id=RULE-0067 -->
```yaml
id: RULE-0067
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0062 via CTRL-0006"
tags: [binding]
claim: SPEC-0062
control: CTRL-0006
enforcement: ENF-0002
relations:
  - { rel: binds, target: SPEC-0062 }
  - { rel: binds, target: CTRL-0006 }
  - { rel: binds, target: ENF-0002 }
```
<!-- atom:end id=RULE-0067 -->

<!-- atom:begin id=RULE-0068 -->
```yaml
id: RULE-0068
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0063 via CTRL-0006"
tags: [binding]
claim: SPEC-0063
control: CTRL-0006
enforcement: ENF-0002
relations:
  - { rel: binds, target: SPEC-0063 }
  - { rel: binds, target: CTRL-0006 }
  - { rel: binds, target: ENF-0002 }
```
<!-- atom:end id=RULE-0068 -->

<!-- atom:begin id=RULE-0069 -->
```yaml
id: RULE-0069
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0065 via CTRL-0005"
tags: [binding]
claim: SPEC-0065
control: CTRL-0005
enforcement: ENF-0002
relations:
  - { rel: binds, target: SPEC-0065 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0002 }
```
<!-- atom:end id=RULE-0069 -->

<!-- atom:begin id=RULE-0070 -->
```yaml
id: RULE-0070
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0066 via CTRL-0002"
tags: [binding]
claim: SPEC-0066
control: CTRL-0002
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0066 }
  - { rel: binds, target: CTRL-0002 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0070 -->

<!-- atom:begin id=RULE-0071 -->
```yaml
id: RULE-0071
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0067 via CTRL-0002"
tags: [binding]
claim: SPEC-0067
control: CTRL-0002
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0067 }
  - { rel: binds, target: CTRL-0002 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0071 -->

<!-- atom:begin id=RULE-0072 -->
```yaml
id: RULE-0072
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0068 via CTRL-0002"
tags: [binding]
claim: SPEC-0068
control: CTRL-0002
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0068 }
  - { rel: binds, target: CTRL-0002 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0072 -->

<!-- atom:begin id=RULE-0073 -->
```yaml
id: RULE-0073
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind RSTR-0015 via CTRL-0002"
tags: [binding]
claim: RSTR-0015
control: CTRL-0002
enforcement: ENF-0001
relations:
  - { rel: binds, target: RSTR-0015 }
  - { rel: binds, target: CTRL-0002 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0073 -->

<!-- atom:begin id=RULE-0074 -->
```yaml
id: RULE-0074
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind RSTR-0016 via CTRL-0002"
tags: [binding]
claim: RSTR-0016
control: CTRL-0002
enforcement: ENF-0001
relations:
  - { rel: binds, target: RSTR-0016 }
  - { rel: binds, target: CTRL-0002 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0074 -->

<!-- atom:begin id=RULE-0075 -->
```yaml
id: RULE-0075
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "Bind SPEC-0069 via CTRL-0007"
tags: [binding]
claim: SPEC-0069
control: CTRL-0007
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0069 }
  - { rel: binds, target: CTRL-0007 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0075 -->
